
function atualizarNumeroItensCarrinho() {
  $.ajax({
    url: '/carrinho/contar',
    type: 'GET',
    success: function(response) {
      var cartCount = response.cart_count;
      $('.cart-quantity').text(cartCount); // Atualiza o número de itens no carrinho
    },
    error: function(error) {
      console.log(error);
    }
  });
}

// Atualiza o número de itens no carrinho quando a página for carregada
atualizarNumeroItensCarrinho();

// Verificar se o usuário está logado
var isUserLoggedIn = false;  // Defina como "true" ou "false" com base na autenticação do usuário

// Função para redirecionar para a página de login
function redirectToLogin() {
  window.location.href = '/login'; // Altere o caminho para a página de login, se necessário
}

// Adicione um manipulador de eventos para capturar o clique no botão "Adicionar ao Carrinho"
$(document).on('click', '.add-to-cart-btn', function(e) {
  e.preventDefault();

  if (isUserLoggedIn) {
    var form = $(this).closest('.add-to-cart-form');
    var produtoId = form.find('input[name="produto_id"]').val();
    var csrfToken = form.find('input[name="csrf_token"]').val();

    // Se o usuário está logado, enviar a requisição para adicionar ao carrinho normalmente
    $.ajax({
      url: '/adicionar_carrinho/' + produtoId,
      type: 'POST',
      headers: {
        'X-CSRFToken': csrfToken
      },
      success: function(response) {
        atualizarNumeroItensCarrinho(); // Atualiza o número de itens no carrinho após adicionar um item
        location.reload(); // Recarrega a página para refletir as alterações no carrinho
      },
      error: function(error) {
        console.log(error);
      }
    });
  } else {
    // Se o usuário não está logado, redirecionar para a página de login
    redirectToLogin();
  }
});

// Adicione um manipulador de eventos para capturar o clique no botão "Cart"
$(document).on('click', '.card-btn', function(e) {
  e.preventDefault();

  if (isUserLoggedIn) {
    window.location.href = '/cart'; // Altere o caminho para a página do carrinho, se necessário
  } else {
    // Se o usuário não está logado, redirecionar para a página de login
    redirectToLogin();
  }
});

// Adicione um manipulador de eventos para capturar o clique no link do carrinho
$('body').on('click', '.cart-link', function(e) {
  e.preventDefault();
  window.location.href = $(this).attr('href');
});

