Part 1: HR sends JD 
     - HR uplods JD.
     - We will create For the class JobD and its schema will be:
          - role
          - Preffered skills 
          - Minimum Experience
          - Educational requirements
          - Responsibilities 
     - Then we need a system prmpt nd will telll the LLM tat you are an expert HR assistant and you have to extract the info based on this schema
     - Now we will give another user_prompt : analyze the following JD pasted by HR 

Part 2: Resume Schema 
     - We will make a class of Experience:
          - company
          - role
          - duration
          - description
          - Skills used
     - Now we will reate our main class Resume:
          - Name 
          - Email
          - Phone
          - Total experiene years
          - Skills -> list
          - Experiences -> list[Experience class we made earlier]
          - Projects -> list[String]
          - certifications -> list[String]
     Remember alll resumes may not have all the fields so we need to handle that too.
     - We will also create a resume schema

Part 3: Read resume
     - Pdf is generally allowed in two formats -> PDF(pdf reader) and word(Document)
     - we will make two functions read_pdf(filepath) and read_docx(filepath)
     - a funtion named read_resume(filepath) if format is pdf return read_pdf() and if format is docx return read_docx()

Part 4: Resume Parsing
     - Resumes folder would have all the resumes and we will iterate on them one by one
     - We will take out the file path
     - resume_text=read_resume() (created before)
     - Now we want a parsed resume so we will crete a fucntion parsed_resume(resume_text) and extrat all the text  

Part 5: Resume Scoring
     - We will create a class MatcResult:
          - score: float
          - details: dictionary
     - a funtion named final_score(job_des,parsed_resume)
     - a user_prompt: You are an HR reruiter and i am giving you job desription and candidate resume mat these two and give a score also give a few details: name, matching skills, missing skills and overall perentage and a short final verdict
      