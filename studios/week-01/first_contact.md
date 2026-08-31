# Week 1 first contact: ELIZA vs. modelo local
## Configuracion
- ELIZA: responder extendido de `starter.py`, usando primero las reglas base y luego tres reglas agregadas.
- Backend del LLM: `ollama`.
- Modelo del LLM: `qwen2.5:1.5b`.
- Prompts: tomados literalmente de `prompts.json`, seccion `first_contact` (7 prompts cualitativos, no un benchmark de 30 instancias).
- Caso de fallo declarado en `starter.py`: `My family is pressuring me and my grades are falling`.

## Transcripcion
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

## Respuestas
### 1. Donde el LLM supera claramente a ELIZA
El LLM supera claramente a ELIZA cuando la entrada pide consejo o contiene contexto que requiere entender mas de una frase. Por ejemplo, cuando se le pregunta si el estudiante deberia abandonar el curso, el LLM responde con una respuesta cautelosa y contextual en vez de una desviacion generica. Tambien puede conectar ansiedad, sueno, estudio y examenes de una forma que ELIZA no puede, porque ELIZA solo compara expresiones regulares.

### 2. Un input donde el fallo del LLM se parece a ELIZA
El prompt "I am my own worst enemy" es el caso del LLM que mas se parece a ELIZA. El LLM da una respuesta fluida y de apoyo, pero se mantiene bastante generica y no sabe realmente que situacion concreta produjo esa frase. Suena util, pero gran parte de la respuesta podria encajar con muchos problemas distintos.

### 3. Que sistema tiene fallos mas faciles de predecir de antemano
Los fallos de ELIZA son mas faciles de predecir porque su comportamiento es solo una lista pequena y ordenada de reglas regex mas un fallback. Si una oracion tiene dos clausulas, una regla first-match puede hacer que la segunda desaparezca, y eso se puede predecir antes de ejecutar el sistema. Esto importa en un sistema real porque los fallos predecibles se pueden probar, documentar y acotar, mientras que los fallos del LLM pueden verse fluidos incluso cuando son vacios o incorrectos.

## Duel Scorecard

| Axis | Classical: ELIZA | LLM: `qwen2.5:1.5b` | Hybrid | Evidence |
|------|------------------|---------------------|--------|----------|
| Correctness | No hay una respuesta correcta unica para todos los prompts; produjo una respuesta fluida en 7/7 prompts, pero perdio contexto importante en casos conocidos. | No hay una respuesta correcta unica para todos los prompts; produjo una respuesta fluida en 7/7 prompts y manejo mejor el consejo/contexto que ELIZA. | No probado. | Transcripcion anterior; `prompts.json`; `test_eliza.py`. Es evidencia cualitativa, no el benchmark exacto de >=30 instancias usado en duelos posteriores. |
| Guarantee | Si una regex coincide, ELIZA devuelve una de las plantillas de esa regla con grupos reflejados; si no, devuelve fallback. No garantiza comprension semantica. | No hay garantia formal antes de ejecutar. El modelo puede responder con fluidez, pero el siguiente prompt similar no esta cubierto por una prueba. | No probado. | `starter.py`; transcripcion anterior. |
| Cost | Un recorrido ordenado de regex mas formato de plantilla; costo local de CPU muy bajo. | Siete llamadas al modelo local; el tiempo total sin cache del LLM fue aproximadamente 143.49s. | No probado. | `.llm_cache/`; corrida local. |
| Latency | Practicamente instantaneo para estos prompts. | 21.09s de mediana / 29.87s p95 en las 7 llamadas sin cache al modelo local. | No probado. | Transcripcion generada con `aicourse.llm`; `.llm_cache/`. |
| Reproducibility | Predecible con orden fijo de reglas y semilla aleatoria fija. | Las salidas cacheadas son reproducibles para esta corrida, pero el modelo en si no tiene una garantia de reglas como ELIZA. | No probado. | Semilla de `eliza.py`; `.llm_cache/`. |
| Scaling | Entradas mas largas o compuestas no aumentan la comprension; first-match-wins puede ignorar clausulas posteriores. | Maneja mejor contexto de lenguaje natural mas largo, pero puede volverse verboso y generico. | No probado. | Prompt compuesto: "My mother is a doctor and my father is a lawyer". En este studio no se corrio una curva por tamano. |
| Interpretability | Alta: podemos senalar la regla regex exacta y la plantilla que se activo. | Baja: la respuesta es texto generado, no un certificado verificable. | No probado. | `starter.py`; `eliza.py`; transcripcion anterior. |
| Failure mode | Fluido pero vacio; la primera regla que coincide puede descartar el resto de la entrada. | Fluido y mas contextual, pero a veces generico o demasiado orientado a consejos de una forma parecida a ELIZA. | No probado. | Caso de fallo declarado; transcripcion anterior. |

## Where we may have been unfair

ELIZA fue extendida con solo tres reglas simples, mientras que el LLM trajo un modelo de lenguaje preentrenado grande a los mismos prompts. Los prompts eran conversacionales y no una tarea con verdad exacta, asi que la correctitud se juzga cualitativamente en vez de con un verificador automatico. Este studio uso 7 prompts compartidos, no el estandar posterior del curso de al menos 30 instancias y una curva de escalamiento. Ademas, el LLM no fue restringido a respuestas cortas, asi que tuvo mas espacio para sonar util que las respuestas basadas en plantillas de ELIZA.
