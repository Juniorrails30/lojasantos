$(document).ready(function() {
  updateCartCount(); // Chama a função para atualizar a contagem do carrinho

  // Função para atualizar a contagem do carrinho
  function updateCartCount() {
    $.ajax({
      url: '/carrinho/contar', // Rota Flask para obter a contagem do carrinho
      type: 'GET',
      success: function(response) {
        $('#cart-count').text(response.count);
      },
      error: function(error) {
        console.log(error);
      }
    });
  }

  // Evento de clique no carrinho
  $('#cart').click(function() {
    window.location.href = '/carrinho'; // Redireciona para a página do carrinho
  });
});

