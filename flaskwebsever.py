from flask import Flask, render_template_string, request, session, redirect, url_for
from ollama import chat
import ollama
import ast
import llm

app = Flask(__name__)
app.secret_key = 'your-secret-key-123'

SECTIONS = [
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

# LLM functions (keep same as before)

BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Verdict Academy</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .container { max-width: 800px; margin: 40px auto; }
        .card { margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .context-box { background: #e9f5ff; padding: 20px; border-radius: 10px; margin-bottom: 25px; }
        .question-box { background: #fff; padding: 20px; border-radius: 10px; margin: 15px 0; }
        pre { white-space: pre-wrap; font-family: inherit; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center mb-4">📖 Verdict Academy</h1>
        {% block content %}{% endblock %}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(BASE_TEMPLATE + '''
        <div class="card">
            <div class="card-body text-center">
                <h2>Welcome to Verdict Academy!</h2>
                <p>Learn about nutrition through interactive lessons</p>
                <a href="{{ url_for('start') }}" class="btn btn-primary">Start Learning</a>
            </div>
        </div>
    ''')

@app.route('/start')
def start():
    session['section_index'] = 0
    session['question_index'] = 0
    session['questions'] = []
    return redirect(url_for('lesson'))

@app.route('/lesson', methods=['GET', 'POST'])
def lesson():
    if 'section_index' not in session:
        return redirect(url_for('home'))
    
    current_section = session['section_index']
    
    if current_section >= len(SECTIONS):
        return redirect(url_for('complete'))
    
    # Generate questions with retry logic
    if not session.get('questions'):
        section_content = SECTIONS[current_section]
        done = False
        while not done:
            try:
                data = llm.gemma3_4(f"for context - {section_content}, make 2 questions THE OUTPUT HAS TO BE IN A python list['question1','question2']")
                modified_string = data[10:-3]
                session['questions'] = ast.literal_eval(modified_string)
                done = True
            except (SyntaxError, ValueError):
                pass
        session['question_index'] = 0
    
    # Rest of the route remains the same
    # ... [keep the existing processing and rendering code]
    
    # Process answers
    feedback = None
    if request.method == 'POST':
        if 'answer' in request.form:
            user_answer = request.form['answer']
            current_question = session['questions'][session['question_index']]
            feedback = llm.gemma3(f"This answer - ({user_answer}) to question ({current_question}) correct? If correct say 'Correct!', if wrong explain why briefly (max 50 chars)")
            session['question_index'] += 1
        else:
            # Move to next section
            session['section_index'] += 1
            session['questions'] = []
            return redirect(url_for('lesson'))
    
    # Check if section complete
    if session['question_index'] >= len(session['questions']):
        return render_template_string(BASE_TEMPLATE + '''
            <div class="card">
                <div class="card-body">
                    <div class="context-box">
                        <h3>Section {{ section_num }} Completed!</h3>
                        <p>You've finished all questions for this section</p>
                    </div>
                    <form method="POST">
                        <button class="btn btn-success" name="next_section">Continue to Next Section</button>
                    </form>
                </div>
            </div>
        ''', section_num=current_section+1)
    
    # Show current lesson
    return render_template_string(BASE_TEMPLATE + '''
        <div class="card">
            <div class="card-body">
                <div class="context-box">
                    <h3>Section {{ section_num }}</h3>
                    <pre>{{ section_content }}</pre>
                </div>
                
                <div class="question-box">
                    <h4>Question {{ question_num }}</h4>
                    {% if feedback %}
                    <div class="alert alert-info mb-3">{{ feedback }}</div>
                    {% endif %}
                    <p>{{ current_question }}</p>
                    <form method="POST">
                        <input type="text" name="answer" class="form-control mb-3" 
                               placeholder="Type your answer..." required>
                        <button class="btn btn-primary">Submit Answer</button>
                    </form>
                </div>
            </div>
        </div>
    ''', 
    section_num=current_section+1,
    section_content=SECTIONS[current_section],
    question_num=session['question_index']+1,
    current_question=session['questions'][session['question_index']],
    feedback=feedback)

@app.route('/complete')
def complete():
    return render_template_string(BASE_TEMPLATE + '''
        <div class="card">
            <div class="card-body text-center">
                <h2>🎉 Course Complete!</h2>
                <p>Congratulations on finishing all modules!</p>
                <a href="{{ url_for('home') }}" class="btn btn-secondary">Start Over</a>
            </div>
        </div>
    ''')

if __name__ == '__main__':
    app.run(debug=True)