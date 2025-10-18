document.addEventListener("DOMContentLoaded", () => {
    const questionEl = document.getElementById("question");
    const optionsEl = document.getElementById("options");

    if (!QUESTION_DATA || !QUESTION_DATA.options) return;

    // Render question
    questionEl.textContent = QUESTION_DATA.question;

    QUESTION_DATA.options.forEach((opt, index) => {
        const btn = document.createElement("div");
        btn.classList.add("option");
        btn.textContent = opt;
        btn.dataset.index = index;
        optionsEl.appendChild(btn);

        btn.addEventListener("click", async () => {
            // Disable further clicks
            document.querySelectorAll(".option").forEach(o => o.style.pointerEvents = "none");

            // Determine if clicked option is correct
            const correctIndex = QUESTION_DATA.correct;
            const correctBtn = document.querySelector(`.option[data-index='${correctIndex}']`);

            if (index === correctIndex) {
                btn.classList.add("correct");
            } else {
                btn.classList.add("incorrect");
                if (correctBtn) correctBtn.classList.add("correct");
            }

            // Wait briefly so user sees feedback colors
            setTimeout(async () => {
                try {
                    await fetch("/quiz", {
                        method: "POST",
                        headers: { "Content-Type": "application/x-www-form-urlencoded" },
                        body: `selected=${index}`,
                    });
                    window.location.reload(); // next question
                } catch (err) {
                    console.error("Failed to submit answer", err);
                }
            }, 1000);
        });
    });
});


