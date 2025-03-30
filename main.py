import llm
import ast

with open('What are Nutrients.txt', 'r', encoding='utf-8') as file:
    # Read the content of the file
    content = file.read()


#llm.gemma3_12(f"""Take the {content} and break it into 3-5 smaller sections. Each section should be a summarized and engaging sub-topic, expanded to 200-250 words. These sections should be easy for students to read and learn from on a website. Provide the output as a Python list, with each section as a string in the list.e""")

sections = [
    """
    **The Shadow of Pellagra: A History of Suffering and Misunderstanding**

    For centuries, pellagra haunted the American South and other parts of the world, leaving a trail of suffering and death. Initially dubbed “Black Tongue” due to the characteristic inflammation of the tongue, pellagra’s symptoms – the “four Ds” (diarrhea, dermatitis, dementia, and death) – terrified communities.  Doctors struggled to understand the disease, attributing it to everything from bad air to moral failings.  
The widespread nature of pellagra, particularly affecting impoverished populations dependent on corn as a 
staple food, initially fueled social stigma and blame rather than a search for a medical explanation.  Rural areas, especially those facing economic hardship and food insecurity, bore the brunt of the epidemic.  
These communities often lacked access to diverse diets and adequate medical care, exacerbating the problem. The impact on children was particularly devastating, leading to high mortality rates and long-term developmental issues for survivors.  Early treatments were largely ineffective, focusing on palliative care rather than addressing the underlying cause. This era of confusion and limited understanding highlighted the 
critical need for scientific investigation into the root of this debilitating condition.

    """,
    """
    **The Corn-Centric Diet and the Emergence of a Hypothesis**

    The connection between corn and pellagra started to become apparent through careful observation.  Doctors noticed a striking correlation: regions where corn was the dominant food source also reported the highest rates of pellagra. While initially, many believed that the corn itself was "bad," some researchers began to suspect that the problem lay in the way the corn was processed or in the overall diet lacking essential nutrients.  Traditional corn nixtamalization – soaking and grinding corn with lime – was a key process developed by indigenous cultures in Mesoamerica.  Nixtamalization significantly improved the nutritional 
value of corn by making niacin (vitamin B3) more bioavailable.  As communities transitioned away from traditional methods, adopting more refined corn products and relying more heavily on cornmeal, the risk of niacin deficiency increased. Early investigations began to suggest that a dietary deficiency could be the culprit. The key was identifying *what* was missing.

    """,
    """
    **Goldberger’s Groundbreaking Research: Challenging Conventional Wisdom**

    Joseph Goldberger, a Public Health Service physician, spearheaded the pivotal research that ultimately unraveled the mystery of pellagra. Goldberger’s work was remarkable for its rigor and willingness to challenge prevailing medical opinions.  He initially questioned the “contagious” theory of pellagra, prevalent at the time, and designed a series of daring experiments to test his hypothesis.  One of his most controversial experiments involved deliberately inducing pellagra in himself and his team by feeding them a diet 
of white corn grits – a stark contrast to the traditional nixtamalized corn diet. This brave, and risky, act allowed Goldberger to carefully document the disease's progression. Importantly, when the team began supplementing their diet with brewer’s yeast, rich in niacin, they recovered.  Goldberger’s work unequivocally demonstrated that pellagra was a nutritional deficiency disease, not a contagious one. Goldberger's work was met with some initial resistance from the medical establishment, but his data were so compelling that they could not be ignored.

    """,
    """
    **The Triumph of Niacin and the Shift in Public Health**

    The identification of niacin as the critical nutrient lacking in pellagra-prone diets led to a rapid and transformative shift in public health interventions. Initially, campaigns focused on encouraging the consumption of foods rich in niacin, such as milk, meat, and eggs. However, these options were often inaccessible to the populations most affected.  A more sustainable solution emerged with the promotion of enriched cornmeal, a cost-effective way to deliver niacin directly to those at risk.  This simple yet effective strategy significantly reduced the incidence of pellagra within a relatively short period.  Furthermore, the understanding of pellagra's nutritional basis expanded awareness of the importance of balanced diets and micronutrient deficiencies in public health.  This triumph underscored the power of scientific investigation and evidence-based interventions in tackling public health crises.  The eradication of pellagra highlighted the critical role of public health initiatives in ensuring access to nutritious foods and promoting 
population health.

    """,
    """
    **Lessons Learned: Science, Society, and the Fight Against Deficiency**

    The story of pellagra provides valuable lessons for modern public health. It highlights the importance of rigorous scientific investigation, the dangers of relying on unfounded theories, and the need for culturally sensitive public health interventions.  The initial failure to recognize pellagra as a nutritional 
deficiency stemmed, in part, from social biases and a lack of scientific understanding of dietary needs. The pellagra experience emphasized the crucial role of nutrition education and the importance of ensuring food security for vulnerable populations. Modern public health challenges, such as iron deficiency and iodine deficiency, echo the lessons learned from pellagra. The story serves as a potent reminder that scientific progress is not always linear, that challenging established beliefs is essential, and that a holistic approach—combining science, social awareness, and equitable access to resources—is key to improving population health.
    """
]

def main():
    for i in sections:
        done = False
        while done == False:
            try:
                data = llm.gemma3_4(f" for context - {i}, make 2 questions THE OUTPUT HAS TO BE IN A python list['question1','question2']")
                modified_string = data[10:-3]
                my_list = ast.literal_eval(modified_string)
                print(i)
                done = True
            except SyntaxError:
                pass

        for q in my_list:
            print(q)
            print("----------------")
            ans = input("What do you think is the answer to this question?  ")
            resp = llm.gemma3(f"This is the answer - ({ans}) provided to the question ({q}) correct? if correct say you are right, if i am wrong tell me why,ALWAYS KEEP RESPONSE UNDER 50 CHAR")
            print(resp)
            

main()