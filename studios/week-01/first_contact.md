# Week 1 first contact: ELIZA vs. local LLM
## Setup
- ELIZA: extended responder from `starter.py`, with base rules first and three added rules.
- LLM backend: `ollama`.
- LLM model: `qwen2.5:1.5b`.
- Prompts: verbatim from `prompts.json` under `first_contact`.
- Failure case declared in `starter.py`: `My family is pressuring me and my grades are falling`.

## Transcript
### Prompt: I am not feeling great about the exam
**you >** I am not feeling great about the exam

**ELIZA >** How long have you been not feeling great about the exam?

**LLM >**

It's completely normal to feel nervous or anxious before an exam. Here are some tips that might help you feel more prepared and confident:

1. **Prepare Well**: Make sure you have studied thoroughly for your exams. This includes understanding the material, practicing problems, and reviewing notes.

2. **Get Enough Sleep**: Ensure you get enough rest leading up to the exam day. Lack of sleep can make you feel tired and less focused during the test.

3. **Eat Healthily**: Eat a balanced meal before the exam. Avoid heavy or fatty foods that might cause indigestion.

4. **Relax Beforehand**: Spend some time relaxing, listening to music, or doing something enjoyable right before the exam. This can help calm your nerves and make you feel more relaxed.

5. **Stay Hydrated**: Drink water throughout the day leading up to the exam. Dehydration can affect your concentration.

6. **Focus on Your Exam**: Try to focus on what is being asked in the exam rather than worrying about how well you will do. This can help reduce anxiety and make the process more manageable.

7. **Take a Deep Breath**: If you feel overwhelmed, take a few deep breaths. This can help calm your nerves temporarily.

Remember, exams are just one part of your academic journey. It's okay to not perform perfectly every time. The important thing is that you've done everything you can to prepare and try your best. Good luck!

### Prompt: I feel anxious most of the time
**you >** I feel anxious most of the time

**ELIZA >** Do you often feel anxious most of the time?

**LLM >**

It's completely normal to feel anxious sometimes, but it can be overwhelming and affect your daily life if you experience it all the time. Here are some tips that might help:

1. Identify what triggers your anxiety: Try to pinpoint specific situations or thoughts that cause you to feel anxious. Understanding what triggers your anxiety can help you avoid those situations or change how you react.

2. Practice relaxation techniques: Deep breathing, meditation, and progressive muscle relaxation can all help reduce anxiety symptoms.

3. Exercise regularly: Physical activity releases endorphins, which are chemicals in the brain that can improve mood and reduce stress.

4. Get enough sleep: Lack of sleep can increase feelings of anxiety. Try to establish a regular sleep routine and stick to it as much as possible.

5. Seek professional help: If your anxiety is severe or interfering with your daily life, consider seeking help from a mental health professional such as a therapist or counselor.

Remember that everyone experiences anxiety at some point in their lives, but if you find yourself feeling anxious most of the time, it's important to seek support and take steps to manage your symptoms.

### Prompt: My mother thinks I should study more
**you >** My mother thinks I should study more

**ELIZA >** Tell me more about your mother.

**LLM >**

I understand that your mother is concerned about your studies and wants you to do better in school. It's important for parents to support their children academically and encourage them to pursue their interests and passions.

If you feel overwhelmed or stressed by the pressure of studying, it might be helpful to talk to your mother about how you're feeling. You could also try setting realistic goals and breaking down larger tasks into smaller, more manageable steps. This can help make studying less overwhelming and increase your motivation to complete assignments on time.

Remember that everyone has different strengths and interests, so don't feel like you have to study in a certain way or follow a specific routine. Find what works best for you and stick with it!

### Prompt: I did badly because I did not sleep
**you >** I did badly because I did not sleep

**ELIZA >** Is that the real reason?

**LLM >**

It's understandable that you feel disappointed after doing poorly on an exam or assignment due to lack of sleep. Sleep is crucial for cognitive function and memory consolidation, which can significantly impact your performance in academic tasks.

Here are a few tips to help improve your sleep quality:

1. Establish a consistent bedtime routine: This helps regulate your body's internal clock.
2. Create a comfortable sleeping environment: Make sure your room is dark, quiet, and cool.
3. Avoid stimulating activities before bed: Limit caffeine, alcohol, and heavy meals.
4. Exercise regularly but avoid vigorous workouts close to bedtime.
5. Practice relaxation techniques like meditation or deep breathing.

If you consistently struggle with sleep, consider speaking with a healthcare professional for further guidance.

### Prompt: Do you think I should drop this course?
**you >** Do you think I should drop this course?

**ELIZA >** What does that suggest to you?

**LLM >**

As an AI language model, I don't have access to your personal situation or the specific details of the course you're referring to. However, in general terms, if you feel that the course is not aligned with your goals, interests, or skills, it might be a good idea to consider dropping it.

Here are some factors to consider:

1. Course relevance: Does this course align with what you want to achieve? If not, it may not be worth investing time and money into.
2. Instructor quality: Is the instructor knowledgeable and experienced in the subject matter?
3. Learning style: Do you learn best through lectures or hands-on practice?
4. Time commitment: How much time do you have available for this course?

If you're unsure whether to drop a course, it might be helpful to speak with someone who has experience in that field or ask your instructor directly about the course's relevance and effectiveness.

Ultimately, the decision is yours, but if you feel strongly that the course isn't right for you, it may be worth considering dropping it.

### Prompt: My mother is a doctor and my father is a lawyer
**you >** My mother is a doctor and my father is a lawyer

**ELIZA >** Tell me more about your mother.

**LLM >**

That's great! It sounds like you have both parents who work in important professions that can provide valuable guidance and support to your life. As for the question about whether or not it's better to be a doctor or a lawyer, there isn't really an easy answer because everyone has their own unique strengths and interests.

Both careers require hard work, dedication, and often long hours. Doctors need to have excellent communication skills, empathy, and strong problem-solving abilities. Lawyers must be able to analyze complex information quickly and effectively present arguments in court.

Ultimately, the choice between a career as a doctor or lawyer depends on your personal preferences, interests, and what you enjoy doing. If you're more interested in helping people and making a difference in their lives through medicine, then becoming a doctor might be a good fit for you. On the other hand, if you're more drawn to using your analytical skills to solve complex problems and advocate for clients' rights, then being a lawyer could be a better choice.

It's also worth considering that both careers can lead to fulfilling and rewarding work, as well as providing opportunities for personal growth and development. So it really comes down to what you enjoy doing the most and what kind of lifestyle you're looking for in your career.

### Prompt: I am my own worst enemy
**you >** I am my own worst enemy

**ELIZA >** Why do you say you are your own worst enemy?

**LLM >**

It's not uncommon to feel like you're your own worst enemy sometimes. This can be due to various reasons such as stress, anxiety, or self-doubt. It's important to recognize these feelings and work on finding ways to manage them effectively.

Here are a few strategies that might help:

1. **Self-Compassion**: Treat yourself with the same kindness you would offer to a friend who was going through a tough time. Remind yourself that everyone has days when they feel like their worst enemy.

2. **Mindfulness and Meditation**: Practice mindfulness or meditation to stay present in the moment, which can help reduce negative self-talk and increase positive thinking.

3. **Journaling**: Write down your thoughts and feelings about challenging situations. This can be a way of processing emotions without immediately reacting to them.

4. **Exercise**: Physical activity can release endorphins, which are chemicals in the brain that act as natural painkillers and mood elevators.

5. **Seek Support**: Talk to friends or family members who understand what you're going through. Sometimes just sharing your feelings with someone else can make a big difference.

6. **Professional Help**: If these feelings become overwhelming, consider seeking help from a therapist or counselor who specializes in dealing with self-doubt and negative thinking patterns.

Remember, it's okay to struggle sometimes, but taking steps to manage these feelings is important for overall well-being.

## Answers
### 1. Where does the LLM obviously beat ELIZA?
The LLM obviously beats ELIZA when the input asks for advice or contains context that requires understanding more than one phrase. For example, when asked whether the student should drop the course, the LLM responds with a cautious, contextual answer instead of a generic deflection. It can also connect anxiety, sleep, studying, and exams in a way ELIZA cannot because ELIZA only matches regular expressions.

### 2. One input where the LLM failure is recognizably ELIZA-like
The prompt "I am my own worst enemy" is the most ELIZA-like LLM case. The LLM gives a fluent and supportive answer, but it stays fairly generic and does not really know what concrete situation produced that sentence. It sounds helpful, yet much of the response could fit many unrelated problems.

### 3. Which system has failures that are easier to predict in advance?
ELIZA failures are easier to predict because its behavior is just a small ordered list of regex rules plus a fallback. If a sentence has two clauses, a first-match rule can make the second clause disappear, and we can predict that before running it. That matters in a shipped system because predictable failures can be tested, documented, and bounded, while LLM failures may look fluent even when they are hollow or wrong.
