<p align="center">
  <img src="assets/smaller.png" alt="Promptly Logo">
</p>

<h1 align="center"><strong>Promptly</strong></h1>

<p align="center">
  🚀 We're launching soon — <strong><a href="https://promtly.tech">join the waitlist</a></strong> to get early access!
</p>

---

# Promptly

Promptly is an AI-driven platform that enables users to create custom chatbots based on their unique datasets. It allows users to upload data, train models, and interact with them through a simple API interface. Whether you're a business looking to automate customer support or a developer wanting to explore RAG-based AI, Promptly is designed to be intuitive, flexible, and powerful.

---

## ⭐️ Show Your Support

If you find **Promptly** helpful or inspiring, please consider giving us a ⭐️ on GitHub!  
Your support helps others discover the project and motivates continued development and improvement.

> Thank you for being part of the journey! 🙌

👉 [**Star this project on GitHub**](https://github.com/SaidiSouhaieb/promptly-lite.git)

[![GitHub Stars](https://img.shields.io/github/stars/SaidiSouhaieb/promptly-ai-backend?style=social)](https://github.com/SaidiSouhaieb/promptly-ai-backend/stargazers)

## 🚀 Features

- **Customizable Chatbots**: Upload your own data to train AI models.
- **Dynamic Interactions**: Create chatbots capable of handling dynamic and evolving queries.
- **Easy API Access**: Interact with your chatbot using simple API calls.
- **Open-Source**: Built to be open and collaborative. [**Contribute here**](CONTRIBUTING.md)
- **Scalable**: Designed to handle varying data sizes and use cases.

## 📂 Installation

### Prerequisites

- Docker
- Docker Compose
- .env file configured (see below)

### Getting Started

1. **Clone the repo**:

```bash
git clone https://github.com/SaidiSouhaieb/promptly-lite.git
cd promptly-ai-backend
```

2. **Build and Run using Docker**:

Use the provided `Makefile` commands to manage the project easily:

- **Build the Docker image**:

```bash
make build
```

- **Start the application in the background**:

```bash
make up
```

- **Stop the application**:

```bash
make down
```

- **Rebuild the Docker container**:

```bash
make rebuild
```

- **View container logs**:

```bash
make logs
```

- **Access backend container shell**:

```bash
make shell-backend
```

3. **Set up environment variables**:

Create a `.env` file in the root of the project and add necessary environment variables:

```env
# Backend
POSTGRES_USER=user_xyz789
POSTGRES_PASSWORD=SecurePass#9876
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=my_test_db
POSTGRES_URL=postgresql://user_xyz789:SecurePass#9876@localhost:5433/my_test_db

# Server
BACKEND_PORT=3000
```

4. **Run Alembic Migrations**:

- Upgrade to latest migration:

```bash
make alembic-upgrade
```

- Downgrade one migration step:

```bash
make alembic-downgrade
```

- Generate new migration file:

```bash
make alembic-revision
```

- Create and apply migration:

```bash
make alembic-migrate
```

5. **Run Tests**:

To run backend tests:

```bash
make test
```

---

4. **Access the Application**:

After starting the container, you can access the application on the specified port (3000 by default) on your local machine.

---

## 📝 How to Contribute

We welcome contributions from everyone! If you'd like to contribute, please follow the steps outlined in our [CONTRIBUTING.md](CONTRIBUTING.md) file.

### Pull Request Process

- Fork the repository
- Clone your fork and create a new branch for your feature or bug fix
- Make your changes and commit them
- Push your changes to your fork
- Open a pull request to the main branch of the original repo

---

## 🔒 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

---

## 📞 Contact

For inquiries or support, please reach out via [saidisouhaiebai@gmail.com](mailto:saidisouhaiebai@gmail.com).

---

## 🔗 Links

- [Promptly Website](https://promtly.tech)
- [GitHub](https://github.com/SaidiSouhaieb)
- [Personal Linkedin](https://www.linkedin.com/in/saidi-souhaieb-4632702a8/)
