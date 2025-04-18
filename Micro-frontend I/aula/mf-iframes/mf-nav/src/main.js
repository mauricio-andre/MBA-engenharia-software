const listaDeLinks = document.querySelector('#lista-de-itens');

window.addEventListener('message', (evento) => {
  if (evento.data.type == 'INICIAR') {
    evento.data.rotas.forEach(rota => {
      const li = document.createElement('li');
      const ancora = document.createElement('a');
      ancora.innerText = rota.nome;

      ancora.addEventListener('click', (evt) => {
        evt.preventDefault();
        window.parent.postMessage({ type: 'NAVEGACAO', destino: rota }, '*');
      });

      ancora.setAttribute('href', rota.path);
      li.appendChild(ancora);
      listaDeLinks.appendChild(li);
    })
  }
});