document.addEventListener("DOMContentLoaded", function() {
    // Handle Cleaner Registration Form Submission
    document.getElementById("cleaner-registration-form").addEventListener("submit", function(event) {
        event.preventDefault();
        
        const cleanerData = {
            name: document.getElementById("name").value,
            age: document.getElementById("age").value,
            experience: document.getElementById("cleaner-experience").value,
            skills: document.getElementById("skills").value,
            location: document.getElementById("cleaner-location").value,
            availability: document.getElementById("availability").value,
        };

        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams(cleanerData),
        })
        .then(response => {
            if (response.ok) {
                alert("Cleaner registered successfully!");
            } else {
                throw new Error("Failed to register cleaner.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("There was an error submitting the registration.");
        });
    });

    // Handle Client Request Form Submission
    document.getElementById("client-request-form").addEventListener("submit", function(event) {
        event.preventDefault();

        const clientRequest = {
            location: document.getElementById("client-location").value,
            experience: document.getElementById("client-experience").value,
            requirements: document.getElementById("requirements").value,
        };

        fetch('/client_request', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams(clientRequest),
        })
        .then(response => {
            if (response.ok) {
                alert("Request submitted successfully!");
            } else {
                throw new Error("Failed to submit request.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("There was an error submitting the request.");
        });
    });

    // Fetch and display the list of cleaners for the admin
    fetch('/admin_cleaners')
        .then(response => response.json())
        .then(cleaners => {
            const cleanerTableBody = document.getElementById("cleaner-list");
            cleaners.forEach(cleaner => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${cleaner.name}</td>
                    <td>${cleaner.age}</td>
                    <td>${cleaner.experience}</td>
                    <td>${cleaner.skills}</td>
                    <td>${cleaner.location}</td>
                    <td>${cleaner.availability}</td>
                `;
                cleanerTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching cleaners:', error);
            alert("There was an error fetching the cleaners data.");
        });

    // Fetch and display the client requests for the admin
    fetch('/admin_client_requests')
        .then(response => response.json())
        .then(clientRequests => {
            const clientRequestTableBody = document.getElementById("client-request-list");
            clientRequests.forEach(request => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${request.location}</td>
                    <td>${request.experience}</td>
                    <td>${request.requirements}</td>
                `;
                clientRequestTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching client requests:', error);
            alert("There was an error fetching the client requests data.");
        });
});
