
console.log("JS LOADED");

document.getElementById("employeeForm").addEventListener("submit", function(event) {
    event.preventDefault();

    console.log("Submit detected");

    const idIdentification = document.getElementById("id_identification").value;
    const fullName = document.getElementById("full_name").value;
    const checkIn = document.getElementById("check_in").value;
    const checkOut = document.getElementById("check_out").value;

    const data = {
        id_identification: parseInt(idIdentification),
        full_name: fullName,
        check_in: checkIn,
        check_out: checkOut
    };

    fetch("/employees", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error sending data");
        }
        return response.json();
    })
    .then(result => {
        document.getElementById("message").textContent = "Employee registered successfully!";
        console.log(result);
    })
    .catch(error => {
        document.getElementById("message").textContent = "Error sending data.";
        console.error(error);
    });
});