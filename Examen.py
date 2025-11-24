# Estructura de datos
library = {
    "books": {},
    "loans": []
}

# Se inicializa con 3 libros pre-cargados
def initialize_books():
    books_data = [
        {
            "title": "The divine comedy", 
            "author": "Dante Alighieri ", 
            "genre": "Epic", 
            "year": 1304, 
            "available": True
        },
        {
            "title": "Blindness essay", 
            "author": "Jose Saramago", 
            "genre": "Fiction", 
            "year": 1995, 
            "available": True
        },
        {
            "title": "1984", 
            "author": "George Orwell", 
            "genre": "Dystopian", 
            "year": 1949, 
            "available": True
        }
    ]
    
    # Se asignan ID a partir del 1 a cada libro registrado
    for i, book in enumerate(books_data, 1):
        library["books"][i] = book

# Funcion que valida el input del usuario
def get_valid_input(prompt, input_type=str, min_value=None, max_value=None):
   
   #Se obtiene y valida  la entrada del usuario con un manejo completo de errores
    while True:
        try:
            user_input = input(prompt).strip()
            
            if input_type == str:
                if not user_input:
                    print("Error: Input cannot be empty")
                    continue
                return user_input
                
            elif input_type == int:
                value = int(user_input)
                if min_value is not None and value < min_value:
                    print(f"Error: Value must be at least {min_value}")
                    continue
                if max_value is not None and value > max_value:
                    print(f"Error: Value must be at most {max_value}")
                    continue
                return value
                
            elif input_type == float:
                value = float(user_input)
                if min_value is not None and value < min_value:
                    print(f"Error: Value must be at least {min_value}")
                    continue
                return value
                
        except ValueError:
            if input_type == int:
                print("Error: Please enter a valid integer")
            elif input_type == float:
                print("Error: Please enter a valid number")

# Funcion para añadir un nuevo libro a la libreria
def add_book():
    
    try:
        print("\n--- Add New Book ---")
        title = get_valid_input("Enter book title: ", str)
        author = get_valid_input("Enter author: ", str)
        genre = get_valid_input("Enter genre: ", str)
        year = get_valid_input("Enter publication year: ", int, 1000, 2025)
        
        # Busca un ID disponible para el nuevo libro agregado
        new_id = max(library["books"].keys()) + 1 if library["books"] else 1
        
        library["books"][new_id] = {
            "title": title,
            "author": author,
            "genre": genre,
            "year": year,
            "available": True
        }
        
        print(f"Book '{title}' added successfully with ID: {new_id}")
        
    except Exception as e:
        print(f"Error adding book: {e}")

#Funcion para mostrar todos los libros agregados
def view_books():
    
    if not library["books"]:
        print("No books available in the library")
        return
    
    print("\n--- All Books ---")
    for book_id, book in library["books"].items():
        status = "Available" if book["available"] else "Borrowed"
        print(f"ID: {book_id} | {book['title']} by {book['author']} | {book['year']} | {status}")

#Funcion para buscar los libros ya agregados
def search_books():
    
    try:
        print("\n--- Search Books ---")
        search_term = get_valid_input("Enter title or author to search: ", str).lower()
        
        found_books = []
        for book_id, book in library["books"].items():
            if (search_term in book["title"].lower() or 
                search_term in book["author"].lower()):
                found_books.append((book_id, book))
        
        if not found_books:
            print("No books found matching your search")
            return
        
        print(f"\nFound {len(found_books)} book(s):")
        for book_id, book in found_books:
            status = "Available" if book["available"] else "Borrowed"
            print(f"ID: {book_id} | {book['title']} by {book['author']} | {status}")
            
    except Exception as e:
        print(f"Error searching books: {e}")


#Funcion para mostrar los libros prestados
def borrow_book():
    
    try:
        print("\n--- Borrow Book ---")
        view_books()
        
        if not library["books"]:
            return
            
        book_id = get_valid_input("Enter book ID to borrow: ", int, 1)
        
        if book_id not in library["books"]:
            print("Error: Book ID not found")
            return
            
        book = library["books"][book_id]
        
        if not book["available"]:
            print("Error: Book is already borrowed")
            return
        
        borrower = get_valid_input("Enter borrower name: ", str)
        loan_days = get_valid_input("Enter loan period (days): ", int, 1, 30)
        
        # Crea un registro del prestamo
        loan = {
            "book_id": book_id,
            "book_title": book["title"],
            "borrower": borrower,
            "loan_date": "2024-01-01",  
            "due_date": f"2024-01-{loan_days + 1}",  
        }
        
        library["loans"].append(loan)
        book["available"] = False
        
        print(f"Book '{book['title']}' borrowed successfully by {borrower}")
        
    except Exception as e:
        print(f"Error borrowing book: {e}")

#Funcion para registrar los libros devueltos
def return_book():
   
    try:
        print("\n--- Return Book ---")
        
        # Encuentra los prestamos activos
        active_loans = [loan for loan in library["loans"] if not loan["returned"]]
        
        if not active_loans:
            print("No active loans found")
            return
            
        print("Active loans:")
        for i, loan in enumerate(active_loans, 1):
            print(f"{i}. {loan['book_title']} - Borrowed by: {loan['borrower']}")
        
        choice = get_valid_input("Select loan to return: ", int, 1, len(active_loans))
        selected_loan = active_loans[choice - 1]
        
        # Marca como libro devuelto y muestra la disponibilidad de este
        selected_loan["returned"] = True
        library["books"][selected_loan["book_id"]]["available"] = True
        
        print(f"Book '{selected_loan['book_title']}' returned successfully")
        
    except Exception as e:
        print(f"Error returning book: {e}")

# Funcion que genera los reportes
def generate_reports():
    
    try:
        print("\n--- Library Reports ---")
        
        # Un recuento total de los libros
        total_books = len(library["books"])
        available_books = sum(1 for book in library["books"].values() if book["available"])
        borrowed_books = total_books - available_books
        
        print(f"Total books: {total_books}")
        print(f"Available books: {available_books}")
        print(f"Borrowed books: {borrowed_books}")
        
        # Muestra los libros por genero con lambda
        genre_groups = {}
        for book in library["books"].values():
            genre = book["genre"]
            genre_groups[genre] = genre_groups.get(genre, 0) + 1
        
        # Se usa lambda para ordenar géneros por conteo
        sorted_genres = sorted(genre_groups.items(), 
                             key=lambda x: x[1], 
                             reverse=True)
        
        print("\nBooks by genre:")
        for genre, count in sorted_genres:
            print(f"{genre}: {count} book(s)")
        
        # Muestra los prestamos activos
        active_loans = [loan for loan in library["loans"] if not loan["returned"]]
        if active_loans:
            print(f"\nActive loans: {len(active_loans)}")
            for loan in active_loans:
                print(f"- {loan['book_title']} (Due: {loan['due_date']})")
        
    except Exception as e:
        print(f"Error generating reports: {e}")

# Muestra las funciones del menu
def book_management_menu():
    """
    Book management submenu
    """
    while True:
        print("\n--- Book Management ---")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Books")
        print("4. Back to Main Menu")
        
        choice = get_valid_input("Select an option: ", str)
        
        if choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            search_books()
        elif choice == "4":
            break
        else:
            print("Invalid option. Please try again.")
#Funcion muestra 2 opciones; devolver un libro o prestar uno
def loans_menu():
    
    while True:
        print("\n--- Loans Management ---")
        print("1. Borrow Book")
        print("2. Return Book")
        print("3. Back to Main Menu")
        
        choice = get_valid_input("Select an option: ", str)
        
        if choice == "1":
            borrow_book()
        elif choice == "2":
            return_book()
        elif choice == "3":
            break
        else:
            print("Invalid option. Please try again.")
#Funcion muestra el menu principal
def main_menu():
    
    print("\n=== Library Management System ===")
    print("1. Book Management")
    print("2. Loans Management")
    print("3. Reports")
    print("4. Exit")
    
    choice = get_valid_input("Select an option: ", str)
    return choice

def main():
   
    try:
        # Inicializa con los libros predefinidos
        initialize_books()
        print("Library system initialized with 3 books")
        
        # Crea un bucle del programa principal
        while True:
            choice = main_menu()
            
            if choice == "1":
                book_management_menu()
            elif choice == "2":
                loans_menu()
            elif choice == "3":
                generate_reports()
            elif choice == "4":
                print("Leaving the system")
                break
            else:
                print("Invalid option. Please try again.")
                
    except Exception as e:
        print(f"Unexpected error: {e}")

#Punto de entrada del programa
if __name__ == "__main__":
    main()
