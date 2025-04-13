# Constants for static parts of the prompt
INSTRUCTIONS = """**Instructions for AI Job Matching System:**
<INSTRUCTIONS> about the candidate profile / skills / experience / location / language proficiencies
"""

CRITERIA = """**Job Matching Criteria:**
<CRITERIA HERE>
"""

OUTPUT_FORMAT = """**Output:**
If the job and internship opportunity is a strong match and meet these criteria, including the job title, company name, location, and a brief description in English of the role. Also calculate a score out of 100 based on the criteria. Ensure each recommendation aligns with the candidate's skills and language proficiencies:
"""

# Function to generate the full prompt
def generate_prompt(job_description: str) -> str:
    return f"{INSTRUCTIONS}\n\n{CRITERIA}\n\n{OUTPUT_FORMAT}input job: \n{job_description}"