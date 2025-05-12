from google.auth import default

def test_auth():
    credentials, project_id = default()
    print("Credentials valid! Project ID:", project_id)

if __name__ == "__main__":
    test_auth()