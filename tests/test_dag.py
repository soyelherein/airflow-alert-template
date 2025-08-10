from airflow.models import DagBag

def test_for_import_errors():
    dags = DagBag(dag_folder="dags", include_examples=False)
    assert dags.import_errors == {}
