// Constants
const BASE_URL = 'http://127.0.0.1:8000';

class InterviewManager {
    constructor() {
        // Initialize DOM elements
        this.initializeElements();
        
        // Initialize state
        this.stream = null;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.recognition = null;
        this.isRecording = false;
        this.completeTranscript = '';
        this.interviewId = null;
        this.currentQuestion = '';
        this.maxQuestions = 2; // Set the maximum number of questions here
        this.currentQuestionIndex = 0;
        
        // Start setup
        this.setup();
    }

    initializeElements() {
        this.video = document.getElementById('userVideo');
        this.micToggle = document.getElementById('micToggle');
        this.cameraToggle = document.getElementById('cameraToggle');
        this.startRecordingBtn = document.getElementById('startRecording');
        this.submitAnswerBtn = document.getElementById('submitAnswer');
        this.nextQuestionBtn = document.getElementById('nextQuestionBtn');
        this.questionElement = document.getElementById('question');
        this.statusIndicator = document.querySelector('.status-indicator');
        this.submitInterviewBtn = document.getElementById('submitInterview');
        
        if (!this.video || !this.questionElement) {
            throw new Error('Required DOM elements not found');
        }
    }

    async setup() {
        try {
            await this.initializeMediaDevices();
            this.initializeSpeechRecognition();
            this.initializeEventListeners();
            await this.startInterview();
        } catch (error) {
            console.error('Setup failed:', error);
            this.showError('Failed to initialize interview. Please check your camera and microphone permissions.');
        }
    }

    async initializeMediaDevices() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: true
            });
            
            this.video.srcObject = this.stream;
            this.video.muted = true; // Prevent feedback
            
            // Initialize MediaRecorder
            this.mediaRecorder = new MediaRecorder(this.stream);
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                }
            };
        } catch (error) {
            throw new Error('Failed to access media devices: ' + error.message);
        }
    }

    initializeSpeechRecognition() {
        if ('webkitSpeechRecognition' in window) {
            this.recognition = new webkitSpeechRecognition();
            this.recognition.continuous = true;
            this.recognition.interimResults = true;
            
            this.recognition.onresult = (event) => {
                let interimTranscript = '';
                let finalTranscript = '';

                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        finalTranscript += event.results[i][0].transcript;
                    } else {
                        interimTranscript += event.results[i][0].transcript;
                    }
                }

                if (finalTranscript) {
                    this.completeTranscript += ' ' + finalTranscript;
                }
            };

            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.showError('Speech recognition error: ' + event.error);
            };
        } else {
            this.showError('Speech recognition is not supported in this browser');
        }
    }

    initializeEventListeners() {
        this.startRecordingBtn.addEventListener('click', () => this.startRecording());
        this.submitAnswerBtn.addEventListener('click', () => this.submitAnswer());
        this.nextQuestionBtn.addEventListener('click', () => this.getNextQuestion());
        this.submitInterviewBtn = document.getElementById('submitInterview');
        this.submitInterviewBtn.addEventListener('click', () => this.submitInterview());
        
        this.micToggle.addEventListener('click', () => this.toggleMicrophone());
        this.cameraToggle.addEventListener('click', () => this.toggleCamera());
    }

    async startInterview() {
        try {
            this.showLoading(true);
            const jobDescription = localStorage.getItem('jobDescription');
            const resumeContent = localStorage.getItem('resumeText');

            if (!jobDescription || !resumeContent) {
                throw new Error('Job description or resume content not found');
            }

            const response = await fetch(`${BASE_URL}/start-interview`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    job_description: jobDescription,
                    resume_content: resumeContent
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (!data.interview_id || !data.question) {
                throw new Error('Invalid response from server');
            }

            this.interviewId = data.interview_id;
            this.currentQuestion = data.question;
            this.questionElement.textContent = this.currentQuestion;
            this.speakQuestion(this.currentQuestion);
            
        } catch (error) {
            console.error('Error starting interview:', error);
            this.showError(`Failed to start interview: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }


    startRecording() {
        if (this.isRecording) return;
        
        try {
            this.isRecording = true;
            this.completeTranscript = '';
            this.audioChunks = [];
            
            this.recognition.start();
            this.mediaRecorder.start();
            
            document.querySelector('.interview-container').classList.add('recording');
            this.startRecordingBtn.disabled = true;
            this.submitAnswerBtn.disabled = false;
            this.statusIndicator.style.display = 'block';
        } catch (error) {
            console.error('Error starting recording:', error);
            this.showError('Failed to start recording');
            this.isRecording = false;
        }
    }

    submitAnswer() {
        if (!this.isRecording) return;
    
        try {
            this.stopRecording();
            if(this.currentQuestionIndex == this.maxQuestions){
                console.log('Interview complete');
                this.submitAnswerBtn.disabled = true;
                this.nextQuestionBtn.disabled = true;
                // Display the thank you dialog
                this.showThankYouDialog();
            }
            else{
            // Prepare the answer data to be sent to the server
            const answerData = {
                interview_id: this.interviewId,
                answer: this.completeTranscript,
                question: this.currentQuestion
            };
    
            // Send the answer data to the server
            this.sendAnswerToServer(answerData);
    
            // Clear the transcript and get the next question
            this.completeTranscript = '';

        }
        } catch (error) {
            console.error('Error submitting answer:', error);
            this.showError('Failed to submit answer');
        }

        
    }
    
    sendAnswerToServer(answerData) {
        // Implement the logic to send the answer data to the server
        // For example, using fetch to make a POST request to the server
        fetch(`${BASE_URL}/next-question`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(answerData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Handle the response from the server
            this.currentQuestion = data.next_question;
            this.questionElement.textContent = this.currentQuestion;
            this.speakQuestion(this.currentQuestion);
    
            // Increment the current question index
            this.currentQuestionIndex++;
    
            // Check if the maximum number of questions has been reached
            if (this.currentQuestionIndex >= this.maxQuestions) {
                // Disable the "Next Question" button
                this.nextQuestionBtn.disabled = true;
                // Add any other logic you want to perform when the interview is complete
                console.log('Interview complete!');
            }
        })
        .catch(error => {
            console.error('Error submitting answer:', error);
            this.showError('Failed to submit answer');
        });
    }
    
    

    async stopRecording() {
        if (!this.isRecording) return;

        try {
            this.isRecording = false;
            this.recognition.stop();
            this.mediaRecorder.stop();
            
            document.querySelector('.interview-container').classList.remove('recording');
            this.startRecordingBtn.disabled = false;
            this.submitAnswerBtn.disabled = true;
            this.statusIndicator.style.display = 'none';
            
        } catch (error) {
            console.error('Error stopping recording:', error);
            this.showError('Error stopping recording');
        }
    }

    toggleMicrophone() {
        const audioTracks = this.stream.getAudioTracks();
        audioTracks.forEach(track => {
            track.enabled = !track.enabled;
        });
        this.micToggle.classList.toggle('disabled');
    }

    toggleCamera() {
        const videoTracks = this.stream.getVideoTracks();
        videoTracks.forEach(track => {
            track.enabled = !track.enabled;
        });
        this.cameraToggle.classList.toggle('disabled');
    }

    speakQuestion(question) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(question);
            speechSynthesis.speak(utterance);
        }
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background-color: #ff4444;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            z-index: 1000;
        `;
        
        document.body.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 5000);
    }

    showLoading(show) {
        let loader = document.querySelector('.loader');
        if (!loader) {
            loader = document.createElement('div');
            loader.className = 'loader';
            document.querySelector('.interview-container').appendChild(loader);
        }
        loader.style.display = show ? 'block' : 'none';
    }

    async submitInterview() {
        try {
            if (this.currentQuestionIndex >= this.maxQuestions) {
                const response = await fetch(`${BASE_URL}/evaluate-interview`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({
                        interview_id: this.interviewId
                    })
                });
    
                if (!response.ok) {
                    throw new Error(`HTTP error ${response.status}`);
                }
    
                const evaluationResult = await response.json();
                console.log('Interview Evaluation Result:', evaluationResult);
    
                // Display the evaluation result to the user
                this.displayEvaluationResult(evaluationResult);
            } else {
                this.showError('Interview not complete. Please answer all the questions.');
            }
        } catch (error) {
            console.error('Error submitting interview:', error);
            this.showError('Failed to submit interview');
        }
    }
    
    showThankYouDialog() {
        const thankYouMessage = "Thank you for completing the interview! Your feedback has been submitted. We appreciate your time and effort.";
        alert(thankYouMessage);
    
        // Use speech synthesis to read the thank you message
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(thankYouMessage);
            speechSynthesis.speak(utterance);
        }
    }
    
    displayEvaluationResult(evaluationResult) {
        // Display the evaluation result to the user
        console.log(`Confidence Score: ${evaluationResult.confidence_score}`);
        console.log(`Communication Score: ${evaluationResult.communication_score}`);
        console.log('Strengths:');
        evaluationResult.strengths.forEach(strength => console.log(`- ${strength}`));
        console.log('Weaknesses:');
        evaluationResult.weaknesses.forEach(weakness => console.log(`- ${weakness}`));
        console.log('Detailed Feedback:', evaluationResult.detailed_feedback);
        console.log('Improvement Suggestions:');
        evaluationResult.improvement_suggestions.forEach(suggestion => console.log(`- ${suggestion}`));

         // Display the evaluation result to the user
        localStorage.setItem('evaluationResult', JSON.stringify(evaluationResult));
        // Open the result.html page
        window.open('result.html', '_blank');
    }
}

// Initialize the interview manager when the page loads
document.addEventListener('DOMContentLoaded', () => {
    try {
        new InterviewManager();
    } catch (error) {
        console.error('Failed to initialize InterviewManager:', error);
        alert('Failed to initialize the interview. Please refresh the page and try again.');
    }
});