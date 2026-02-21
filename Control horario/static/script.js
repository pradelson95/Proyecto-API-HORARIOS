console.log("JS LOADED");

const form = document.getElementById("employeeForm");
const messageBox = document.getElementById("message");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    // 🔹 Limpiar mensajes anteriores
    messageBox.textContent = "";
    document.querySelectorAll(".error-message").forEach(el => {
        el.textContent = "";
    });

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

    try {
        const response = await fetch("/employees", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        // 🔴 Si hay error de validación (422)
        if (!response.ok) {
            if (result.detail) {
                result.detail.forEach(error => {
                    const field = error.loc[1];  // nombre del campo
                    const message = error.msg;

                    const errorElement = document.getElementById(`${field}_error`);
                    if (errorElement) {
                        errorElement.textContent = message;
                    }

                    // Marcar el campo en rojo
                    const inputElement = document.getElementById(field);
                    if (inputElement) {
                        inputElement.style.border = "2px solid red";
                    }
                });
            } else {
                messageBox.textContent = "Unexpected error occurred.";
            }
            return;
        }

        // 🟢 Si todo salió bien
        messageBox.textContent = "Employee registered successfully!";
        form.reset();

        console.log(result);

    } catch (error) {
        messageBox.textContent = "Server connection error.";
        console.error(error);
    }
});