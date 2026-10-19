function renderizaResumo(produtos) {
  const resumo = produtos.reduce(
    (acumulador, produto) => {
      const qtd = Number(produto.quantidade) || 0;
      const preco = Number(produto.preco) || 0;

      acumulador.itens += qtd;
      acumulador.valorTotal += preco * qtd;
      return acumulador;
    },
    { itens: 0, valorTotal: 0 },
  );

  document.getElementById("resTotal").textContent =
    produtos.length.toLocaleString("pt-BR");
  document.getElementById("resItens").textContent =
    resumo.itens.toLocaleString("pt-BR");
  document.getElementById("resValor").textContent =
    resumo.valorTotal.toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
    });
}

function renderizaTabela(produtos) {
  const tabela = document.getElementById("tabelaProdutos");

  const ordenados = [...produtos].sort((a, b) =>
    a.nome.localeCompare(b.nome, "pt-BR", { sensitivity: "base" }),
  );

  tabela.innerHTML = ordenados
    .map((produto) => {
      return `
  <tr>
    <td>${escapaHtml(produto.nome)}</td>
    <td>${produto.quantidade}</td>
    <td>${Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(normalizaValor(produto.preco))}</td>
    <td>
      <button
        class="btn btn-sm btn-outline-primary me-2"
        data-bs-toggle="modal"
        data-bs-target="#modalEditProduto"
        data-id="${produto.id}"
        data-nome="${escapaHtml(produto.nome)}"
        data-descricao="${escapaHtml(produto.descricao)}"
        data-preco="${produto.preco}"
        data-quantidade="${produto.quantidade}"
      >
        <i class="bi bi-pencil-square"></i>
      </button>
      <button
        class="btn btn-sm btn-outline-danger"
        data-bs-toggle="modal"
        data-bs-target="#modalRmProduto"
        data-id="${produto.id}"
        data-nome="${escapaHtml(produto.nome)}"
      >
        <i class="bi bi-trash3"></i>
      </button>
    </td>
  </tr>
  `;
    })
    .join("");

  function escapaHtml(texto = "") {
    return String(texto)
      .replace(/&/g, "&amp;")
      .replace(/"/g, "&quot;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function normalizaValor(valor = "") {
    return Number(String(valor).replace(",", "."));
  }
}

function configuraBusca(produtos) {
  const inputBusca = document.getElementById("busca");

  inputBusca.oninput = () => {
    const termo = normaliza(inputBusca.value.trim());
    const filtrados = produtos.filter((produto) =>
      normaliza(produto.nome).includes(termo),
    );
    renderizaTabela(filtrados);
  };

  function normaliza(texto) {
    return texto
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase();
  }
}

async function buscaTodosProdutos() {
  const limit = 100;
  const todos = [];

  for (let page = 1; ; page++) {
    const resposta = await fetch(`/api/produtos?page=${page}&limit=${limit}`, {
      method: "GET",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
    });

    if (!resposta.ok) {
      throw new Error(`Erro ${resposta.status} na página ${page}`);
    }

    const itens = await resposta.json();
    todos.push(...itens);

    // Última página
    if (itens.length < limit) {
      break;
    }
  }

  return todos;
}

function temProdutos(produtos) {
  return Array.isArray(produtos) && produtos.length > 0;
}

async function recarregaTabelaProdutos() {
  try {
    const produtos = await buscaTodosProdutos();

    if (!temProdutos(produtos)) {
      msgVazia.classList.remove("d-none");
      renderizaResumo([]);
      document.getElementById("tabelaProdutos").innerHTML = "";
    } else {
      msgVazia.classList.add("d-none");
      renderizaResumo(produtos);
      renderizaTabela(produtos);
      configuraBusca(produtos);
    }
  } catch (erro) {
    console.error(`Falha ao carregar dados dos produtos [${erro}]`);
    mostraToast(
      "Não foi possível carregar os produtos. Tente novamente mais tarde.",
      "danger",
    );
  }
}

const usuario = JSON.parse(localStorage.getItem("usuario"));
if (!usuario) {
  window.location.href = "index.html";
}

document.getElementById("nomeUsuario").textContent = usuario.nome;
recarregaTabelaProdutos();
