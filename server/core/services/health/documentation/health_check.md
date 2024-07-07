## Overview for '/api/health'
The health check endpoint is designed to verify the operational status of the API. It provides a simple and quick way to check if the service is up and running. This endpoint is useful for monitoring and automated deployment systems to ensure that the application is healthy and accessible.

### Endpoint
- **URL:** `/api/health`
- **Method:** `GET`
- **Response:**
  - **Status Code:** `200 OK`
  - **Content-Type:** `application/json`
  - **Body:** Please check the response schemas below.

### Usage
Use this endpoint to:
- Check the health of the API.
- Integrate with monitoring tools to track the status of the service.
- Verify that the service is running correctly after deployment or during routine checks.
