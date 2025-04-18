const rotas = [
  {
    path: '',
    module: 'mf-busca'
  },
  {
    path: '/pedidos',
    module: 'mf-pedidos'
  }
];

const container = document.querySelector('#app');

document
  .querySelectorAll('nav ul li a')
  .forEach(ancora => {
    ancora.addEventListener('click', async function (evento) {
      evento.preventDefault();
      const path = this.getAttribute('href');
      const mfAlvo = rotas.find(mf => mf.path == path);
      const { renderizar } = await import(mfAlvo.module);
      renderizar(container);
    });
  });