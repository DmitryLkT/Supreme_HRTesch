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
