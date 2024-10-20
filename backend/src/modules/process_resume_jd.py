from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI


# Load environment variables from .env
load_dotenv()

def process_resume_and_job_description(resume_text, job_description):
    # Create a ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o")

    # Define prompt templates (no need for separate Runnable chains)
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a comedian who tells jokes about {topic}."),
            ("human", "Tell me {joke_count} jokes."),
        ]
    )

    # Create the combined chain using LangChain Expression Language (LCEL)
    chain = prompt_template | model | StrOutputParser()
    # chain = prompt_template | model

    # Run the chain
    result = chain.invoke({"topic": "lawyers", "joke_count": 3})

    # Output
    print(result)



if __name__ == "__main__":
    jd = """As an intern at NVIDIA, you will collaborate with a team of talented engineers tackling some of
the most complex challenges in cutting-edge technology. Mentored by the best minds in the
industry, you will have the opportunity to make meaningful contributions to exciting and
impactful projects.
As a Software Engineering Intern, the candidate will be responsible for supporting in design and
development of software solutions in the areas of Chip Resource Manager, Graphics, Video, 2D
and 3D graphics under OpenGL and DirectX, ISP, driver stacks for Windows and Linux OS. We
are looking for Interns who are passionate about working at the intersection of leading-edge
graphics, multimedia and operating system software. We are hiring for roles within different
verticals: Cloud, System Software, Infrastructure, AI/ML and Full Stack Development. As an
NVIDIAN, you'll be immersed in a diverse, supportive environment where everyone is inspired to
make a lasting impact on the world.

What you'll be doing
 Principles of hardware operation: CPU and memory architecture, buses and
interconnects
 Operating System fundamentals: multi-processing and scheduling, memory
management, privilege modes, file systems and device drivers
 Algorithms and data structures
 Principles of parallel computing
 C and/or C++ programming languages
What we need to see
 Strong academic background
 Pursuing M. tech/BTech in Computer Science or E&C
 Strong C/C++ programming skills
 Good understanding of programming languages and processor architecture
 Good understanding of Operating System Fundamentals.
 Knowledge of Linux kernel is a plus
 Knowledge of scripting (Python / PERL knowledge) is preferred
 Candidates should have a solid background in Operating System, Algorithm
development
 Knowledge on Object-oriented programming is highly a plus in C / C++ Or Java
 Aptitude in innovative and optimal designs

Ways to stand out from the crowd
 Exposure to Digital Systems, Computer Architecture, Computer Arithmetic, Software
Engg.,
 C & C++ programming languages, assembly language programming, system level
integration & system level programming is preferred.
 Good communications skills and ability and desire to work as a team player are a must.
NVIDIA is widely considered to be one of the world’s most desirable employers. We have some of
the most brilliant and talented people in the world working for us. If you're creative and
passionate about new technology, then this is the place for you!
We are an equal opportunity employer and value diversity at our company. We do not
discriminate on the basis of race, religion, color, national origin, gender, sexual orientation, age,
marital status, veteran status, or disability status. 
"""

    resume_text = "sd"

    print(resume_text)

    # question = generate_que(resume, jd)
    # print(question)
