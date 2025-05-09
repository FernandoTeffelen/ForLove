function calcularTempo(dataString, elementoId) {
    function atualizar() {
        const agora = new Date();
        const evento = new Date(dataString);
        let diff = agora - evento;

        if (diff < 0) return;

        let segundos = Math.floor(diff / 1000);
        const anos = Math.floor(segundos / (365.25 * 24 * 3600));
        segundos %= 365.25 * 24 * 3600;
        const meses = Math.floor(segundos / (30.44 * 24 * 3600));
        segundos %= 30.44 * 24 * 3600;
        const dias = Math.floor(segundos / (24 * 3600));
        segundos %= 24 * 3600;
        const horas = Math.floor(segundos / 3600);
        segundos %= 3600;
        const minutos = Math.floor(segundos / 60);
        segundos %= 60;

        document.getElementById(elementoId).textContent =
            `${anos} anos, ${meses} meses, ${dias} dias, ${horas} horas, ${minutos} minutos e ${segundos} segundos...`;
    }

    atualizar();
    setInterval(atualizar, 1000);
}

// Adicionar novos campos de imagem
document.addEventListener("DOMContentLoaded", function () {
    const maxImagens = 5;
    const imageFields = document.getElementById("image-fields");
    const addBtn = document.getElementById("add-image");

    addBtn.addEventListener("click", () => {
        const inputs = imageFields.querySelectorAll("input[type='file']");
        if (inputs.length >= maxImagens) return;

        const div = document.createElement("div");
        div.classList.add("image-upload");

        const input = document.createElement("input");
        input.type = "file";
        input.name = "imagens";
        input.accept = "image/*";

        div.appendChild(input);
        imageFields.appendChild(div);

        if (imageFields.querySelectorAll("input[type='file']").length >= maxImagens) {
            addBtn.style.display = "none";
        }
    });
});
