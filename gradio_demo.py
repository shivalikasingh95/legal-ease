import gradio as gr
import legal_funcs

qa_demo = gr.Interface( 
              title = "Legal-Ease",
              description="<html><img src='flc_design4.png', alt='Legal-ease logo', width=100, height=100><br>For all your legalese...</html>",
              fn=legal_funcs.question_answer, 
              inputs=[
                     gr.Text(label= "Context", lines=20), 
                     gr.Text(label= "Question")
                    ], 
              outputs=[
                        gr.Text(label='Answer')
                        ]
            )

summarize_demo = gr.Interface(
                    title = "Legal-Ease",
                    description="<html><img src='flc_design4.png', alt='Legal-ease logo', width=100, height=100><br>For all your legalese...</html>",
                    fn=legal_funcs.dummy_fn,
                    inputs=[gr.Text(label='Document', lines=30)],
                    outputs=[gr.Text(label = "Summary", lines=30)]
                )

gr.TabbedInterface(
    [qa_demo, summarize_demo], ["QA", "Summarize"]
).launch()