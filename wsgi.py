"""Module containing the main app instance."""
import department_app as dep


app = dep.create_app()
if __name__ == "__main__":
    app.run()
