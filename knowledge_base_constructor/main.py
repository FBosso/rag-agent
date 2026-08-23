from config import slugify_person
from knowledge_base_constructor.graph import app


def main() -> None:
    print("Knowledge base constructor — research a public person from the web.")
    name = input("First name: ").strip()
    surname = input("Surname: ").strip()
    description = input("Optional short description (press enter to skip): ").strip()

    person_id = slugify_person(name, surname)
    print(f"\nResearching {name} {surname} (3 searches run in parallel, this may take a minute)...\n")

    app.invoke(
        {
            "name": name,
            "surname": surname,
            "description": description,
            "person_id": person_id,
            "collected_documents": [],
        }
    )
    print(f"\nDone. Use the knowledge_base_exploiter to chat about {name} {surname}.")


if __name__ == "__main__":
    main()
