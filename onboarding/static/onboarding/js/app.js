// Только визуализация прогресса. Сохранение данных выполняет Django.
document.querySelectorAll('.ring[data-progress]').forEach(ring => {
    const circle = ring.querySelector('.fg');
    if (!circle) return;
    const percent = Math.max(0, Math.min(100, Number(ring.dataset.progress) || 0));
    const length = 2 * Math.PI * Number(circle.getAttribute('r'));
    circle.style.strokeDasharray = String(length);
    circle.style.strokeDashoffset = String(length);
    requestAnimationFrame(() => requestAnimationFrame(() => {
        circle.style.strokeDashoffset = String(length * (1 - percent / 100));
    }));
});

// Проверка ответа
document.querySelectorAll(".question-form").forEach(form => {
    const button = form.querySelector('button[type="submit"]');
    if (!button) return;

    const result = document.createElement("p");
    result.className = "answer-feedback";
    result.setAttribute("role", "status");
    result.setAttribute("aria-live", "polite");
    result.hidden = true;
    form.appendChild(result);

    let sending = false;

    // Убираем старый результат при выборе другого варианта.
    form.addEventListener("change", () => {
        result.hidden = true;
        result.textContent = "";
    });

    form.addEventListener("submit", async event => {
        event.preventDefault();

        if (sending || !form.reportValidity()) return;

        sending = true;

        const originalText = button.textContent;
        const fields = form.querySelector("fieldset");

        // Собираем данные до отключения полей.
        const data = new FormData(form);

        button.disabled = true;
        button.textContent = "Проверяем…";
        if (fields) fields.disabled = true;

        result.hidden = true;
        form.setAttribute("aria-busy", "true");

        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: data,
                credentials: "same-origin",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "Accept": "application/json",
                },
            });

            if (response.redirected) {
                throw new Error(
                    "Возможно, сессия закончилась. Обнови страницу и войди снова."
                );
            }

            const contentType =
                response.headers.get("content-type") || "";

            if (!contentType.includes("application/json")) {
                throw new Error(
                    "Не удалось проверить ответ. Обнови страницу и попробуй снова."
                );
            }

            const answer = await response.json();

            if (!response.ok) {
                throw new Error(
                    answer.error || "Не удалось проверить ответ."
                );
            }

            result.className = answer.is_correct
                ? "answer-feedback success"
                : "answer-feedback error";

            result.textContent = answer.message;
            result.hidden = false;
        } catch (error) {
            result.className = "answer-feedback error";
            result.textContent = error.message ||
                "Ошибка соединения. Попробуй ещё раз.";
            result.hidden = false;
        } finally {
            button.disabled = false;
            button.textContent = originalText;
            if (fields) fields.disabled = false;

            form.removeAttribute("aria-busy");
            sending = false;
        }
    });
});

// анимация страницы
(() => {
    if (!document.querySelector(".checklist")) return;

    if (
        !("IntersectionObserver" in window) ||
        window.matchMedia("(prefers-reduced-motion: reduce)").matches
    ) {
        return;
    }

    const blocks = document.querySelectorAll(
        ".hero-step, .checklist .step, .progress-grid .card, .pulse"
    );

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("is-visible");
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.02,
        rootMargin: "0px 0px -40px 0px"
    });

    blocks.forEach(block => {
        if (block.getBoundingClientRect().top < window.innerHeight - 40) {
            return;
        }

        block.classList.add("reveal-on-scroll");
        observer.observe(block);
    });
})();