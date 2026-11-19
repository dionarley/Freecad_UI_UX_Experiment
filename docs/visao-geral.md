# Visão Geral — FreeCAD UI/UX Experiment

Este repositório é um laboratório de experimentos de UI/UX para o FreeCAD. O
objetivo é testar se o FreeCAD é viável para customizar a interface (esconder
docks, aplicar QSS, menu contextual rápido, gerenciar docks, editar estilos ao
vivo) e, se der certo, enviar melhorias para a comunidade.

> p.s. i'm not a good programmer yet, and i'm portuguese native speaking.  
> by Dionatley R V  
> God And Odin Bless us !

## O que está neste repositório

| Arquivo | Descrição |
|---|---|
| `ui_lab_probe.py` | Script de "laboratório" de UI dentro do FreeCAD: lista docks, aplica layout/QSS, menu rápido (`Ctrl+Shift+Space`) e restaura o estado original. |
| `ui_lab_app.py` | **Aplicação real de UI/UX** (não só teste): janela com abas de Docks, QSS/Estilo e Info/Controle, log integrado, ícone programático e configuração persistente. |
| `window_test.py` | Janela simples com botão de teste, compatível com o FreeCAD (dentro ou fora). |
| `tests/` | Testes automatizados com pytest (mínimo, sem ocupar muito disco). |
| `run.sh` | Script de execução para sincronizar dependências, rodar testes e executar o app. |
| `Dockerfile` / `.dockerignore` | Container mínimo (podman/docker) para rodar os testes. |
| `pyproject.toml` / `uv.lock` | Gerenciamento de dependências com `uv`. |
| `.mise.toml` | Fixação do Python 3.11 via `mise`. |
| `LICENSE` | Licença CC BY 4.0. |

## Dois modos de uso

1. **Dentro do FreeCAD**: o script se acopla à janela principal do aplicativo e
   pode listar/esconder docks reais, aplicar QSS na MainWindow, recalcular
   documentos, etc.
2. **Fora do FreeCAD (standalone)**: cria sua própria janela independente para
   desenvolver e testar a interface sem precisar do FreeCAD instalado.

## Código original intocado

O arquivo `ui_lab_probe.py` nunca é modificado por outros arquivos do projeto.
Todas as funcionalidades novas (`ui_lab_app.py`, `window_test.py`, testes) são
arquivos autônomos que importam `ui_lab_probe.py` apenas quando necessário, sem
alterá-lo.
