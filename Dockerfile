FROM python:alpine

# Install required packages
RUN apk add --no-cache curl

# Copy the dummy controller
COPY dummy-controller.py /controller.py
RUN chmod +x /controller.py

# Expose port
EXPOSE 8080

# Run the controller
CMD ["python", "/controller.py"]
