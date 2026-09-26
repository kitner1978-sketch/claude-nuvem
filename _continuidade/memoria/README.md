# Memória do Claude Code (copiada do Mac original)

O Claude Code guarda uma "memória" por pasta de projeto em `~/.claude/projects/<caminho-da-pasta>/memory/`. Ela **não viaja** com o projeto. Estes arquivos são a cópia dessa memória em 24/09/2026.

| Pasta | Origem no Mac | Conteúdo |
|---|---|---|
| `projeto_livro/` | `~/.claude/projects/-Volumes-seagate-Projeto-Livro/memory/` | Memória deste livro. `MEMORY.md` é o índice; cada arquivo é um fato, com **Why** e **How to apply** |
| `projeto_irmao_aposentadoria_especial/` | `~/.claude/projects/-Volumes-Macintosh-NVMe-aposentadoria-especial/memory/` | Memória de outro livro do autor (recorte "Aposentadoria Especial"). Serve de contexto: mesma regra de escrita, mesmo gerador de DOCX. **Atenção:** a memória `adi-6309-idade-minima.md` registrou relator e data da ADI 6.309 lidos de um recorte errado do Informativo 1220; a nota de correção está no próprio arquivo |
| `regras_de_trabalho_do_usuario.md` | trecho de `~/.claude/PROJETOS.md` | Quem é o usuário e as regras transversais (verificação antes de afirmar, escrita, recursos da máquina, permissões) |

## Precisa instalar?

Não. O essencial destas memórias já está em `../LEIA_PRIMEIRO.md`, que o `CLAUDE.md` da raiz carrega automaticamente. Se quiser que o Claude Code do outro computador as trate como memória própria:

1. Abra uma sessão do Claude Code na raiz desta cópia (a pasta `projeto_livro`).
2. Veja o nome da pasta que ele criou em `~/.claude/projects/` (é o caminho da pasta com `/`, `\`, `:` e espaços trocados por `-`).
3. Copie os arquivos de `projeto_livro/` para `~/.claude/projects/<essa-pasta>/memory/`.

Os caminhos citados nas memórias (`/Volumes/2tb/...`, `/Volumes/seagate/...`) são do Mac original. A correspondência está em `../LEIA_PRIMEIRO.md`, seção "Mapa de caminhos".
