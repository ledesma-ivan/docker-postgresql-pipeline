import subprocess

def test_pipeline():
    # Specifies the full path to the file 'pipeline.py'if located outside the test directory
    result = subprocess.run(['python', '/home/ivan/Escritorio/docker-postgresql-pipeline/pipeline.py', '29-03-23'], capture_output=True, text=True)
    # Verify expected output
    assert result.stdout.strip() == 'job finished = 29-03-23'
