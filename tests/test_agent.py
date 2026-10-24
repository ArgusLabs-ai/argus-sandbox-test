from agent import app


def test_refund_question_gets_an_answer():
    result = app.invoke({"question": "How long does a refund take?"})
    assert result["answer"]


def test_shipping_question_gets_an_answer():
    result = app.invoke({"question": "When will my shipping update arrive?"})
    assert result["answer"]
