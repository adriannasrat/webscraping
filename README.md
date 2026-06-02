# Lab 5 – Web Scraping REST API

This project was completed as part of the **Script Programming** course at Dalarna University.

The lab was structured as an agile mini-project where the goal was to design and implement a REST API for a fictional client, **Bokfirman Ruffel och Bok**. The API retrieves book categories and book information from the website *books.toscrape.com*, stores the data in JSON files, and supports CRUD operations.

---

## Project Overview

The client requested a web scraping solution capable of:

- Retrieving book categories and category URLs
- Scraping books from a selected category
- Storing scraped data in JSON files
- Performing CRUD operations through a REST API
- Reusing previously scraped data when possible
- Converting prices from GBP to SEK using live exchange-rate data
- Deploying the application for external testing

The requirements were intentionally vague to simulate a real-world client engagement where clarification, interpretation and requirement analysis were part of the assignment.

---

## Agile Development Process

The project followed a simplified Scrum workflow.

### Kanban Board (Trello)

The development process was organized using:

- Backlog (Product Backlog Items)
- Sprint Planning / To Do
- Doing
- Testing / Review
- Done

User stories were created based on interpreted customer requirements and tracked throughout development.

### Sprint Review

The project concluded with a demonstration where the completed functionality was tested and presented using Postman.

---

## Features

### Category Scraping

- Scrapes all available book categories
- Stores category names and URLs in JSON format
- Reuses stored category data when available

### Book Scraping

- Retrieves all books within a selected category
- Extracts:
  - Title
  - Price
  - Rating
- Saves results in dated JSON files

Example:

```text
history_260305.json
science_260305.json
mystery_260305.json
```

### Smart Data Caching

To avoid unnecessary scraping:

- Existing JSON files are checked first
- If data already exists for the current date:
  - JSON data is returned directly
- Otherwise:
  - A new web scrape is performed
  - A new JSON file is generated

### Currency Conversion

Book prices are:

- Scraped in British Pounds (£)
- Converted into Swedish Kronor (SEK)
- Stored alongside the original price

### Regular Expressions

Regular expressions were used to:

- Clean scraped price values
- Remove unwanted characters
- Extract structured data from HTML content

---

## REST API

The API supports CRUD operations through standard HTTP methods.

### GET

Retrieve:

- Categories
- Category URLs
- Books in a category

### POST

Create:

- New categories
- New book entries

### PUT

Update:

- Existing category information
- Existing book information

### DELETE

Remove:

- Categories
- Book records

Data is persisted using JSON files rather than a traditional database.

---

## Technologies Used

- Python
- Flask
- BeautifulSoup
- Requests
- JSON
- Regular Expressions (Regex)
- Trello
- Postman

---

## Skills Practiced

- Web Scraping
- REST API Development
- CRUD Operations
- JSON Data Persistence
- Agile Development
- Scrum & Kanban
- API Testing with Postman
- Data Cleaning using Regex
- Requirement Analysis
- Python Backend Development

---

## Learning Outcomes

This project combined several topics from the course into a single application. Beyond web scraping and API development, it provided experience in working with incomplete requirements, planning development work using agile methods, testing APIs, and designing a maintainable solution for a real-world-inspired business case.
