# Work Experience (Frontend)

Welcome to the Work Experience (Frontend) project, a Nuxt 3 application designed to showcase a portfolio of my life's work across various technologies. Initially created as a personal tool to quickly find projects built with different technologies, it has evolved into a comprehensive display of my professional journey.

## Live Demo

Visit [experience.josephpickering.co.uk](experience.josephpickering.co.uk) to see the project in action.

## Overview

This project leverages the power of Nuxt 3, Tailwind CSS, and daisyUI library to provide a server-side rendered application with a focus on aesthetics and responsiveness. It's designed to improve SEO and meta information management, ensuring that my work is not only showcased but also easily discoverable.

### Features

- **Server-Side Rendering (SSR):** Ensures faster load times and better SEO performance.
- **Tailwind CSS & daisyUI:** Utilized for rapid UI development with a focus on design and customization.
- **SEO & Meta Tag Management:** Enhances visibility and searchability on the web.
- **Deployment:** Automated deployment on a Digital Ocean droplet via GitHub Actions for continuous integration and delivery.
- **Linting with Husky:** Enforces code quality and style consistency.
- **TypeScript Code Generation:** Utilises `openapi-typescript-codegen` to automatically generate TypeScript definitions from Swagger documentation.
- **Integration with Work Experience (API):** This frontend is connected to a dedicated API service, providing dynamic data and interaction capabilities.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/josephpickering9/work-experience.git
   cd work-experience
   ```

2. **Install Dependencies:**

   ```bash
   yarn install
   ```

3. **Initial Configuration:**

   After installation, you may need to configure environment variables or other settings specific to your development environment. Create a .env file (using .env.example) at the root of your project and fill it with necessary configurations, such as API endpoints or keys.

4. **Running the project:**

   With dependencies installed, linting configured, and TypeScript types generated, you're now ready to run the project locally:

   ```bash
   yarn dev
   ```

## Linting

To maintain high code quality and consistency across the project, linting is enforced using Husky. This setup ensures that all commits meet our code standards before they can be pushed to the repository.

```bash
# lint on updated files
$ yarn lint

# lint on all files
$ yarn lint:full

# lint & fix errors
$ yarn lint --fix
```

## OpenAPI Codegen

This project uses the openapi-typescript-codegen package to automatically generate TypeScript interfaces and types from the Swagger documentation provided by the Work Experience (API) project. This process ensures type safety and accelerates development by providing auto-completion and validation based on the API's schema.

```bash
# generate files
$ yarn codegen

# fetch latest swagger.json and generate files
$ yarn fetch-codegen
```

## Deployment

The project is configured for deployment on a Digital Ocean droplet via GitHub Actions. To deploy your changes, simply push to the `develop` branch, and the CI/CD pipeline will handle the rest.
