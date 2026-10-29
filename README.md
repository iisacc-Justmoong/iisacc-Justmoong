# Muyeong Yun · Justmoong

**Product Engineer — creative software, C++ systems, and product UI**

I build [iisacc](https://iisacc.com/), an independent creative-software ecosystem. My work connects product requirements and interface design with application architecture, reusable SDKs, and the practical details of packaging and operation.

I focus on tools that let people create, inspect, organize, and preserve their work. My background in e-commerce, visual design, and content operations also informs how I approach user workflows and product decisions.

**Open to remote opportunities in product engineering, desktop application development, and design engineering.**

## What I work on

- **Creative applications:** generation and review workflows, document editing, previews, and reusable canvas systems.
- **C++ foundations:** explicit ownership, observable state, asynchronous work, module boundaries, and CMake package integration.
- **Product UI:** information hierarchy, interaction states, declarative components, and the connection between design and implementation.
- **Local AI and data:** agent orchestration, source-aware retrieval, file identity, revisions, and shared application storage.
- **Web products:** SvelteKit and React interfaces, service integration, and customer-facing product flows.

## Selected projects

| Project | Focus |
| --- | --- |
| [Dreamscapes](https://github.com/iisacc-Justmoong/Dreamscapes) | Creative application connecting image/video generation, result review, canvas editing, and Society-backed storage. |
| [Society](https://github.com/iisacc-Justmoong/Society) | Content and storage workflows built around managed originals, file identity, revision history, and shared logical disks. |
| [iiSDKCore](https://github.com/iisacc-Justmoong/iiSDKCore) | C++23 foundation for application lifetime, execution, and typed observable state, with explicit boundaries between contracts and runtime services. |
| [iiSharedCanvas](https://github.com/iisacc-Justmoong/iiSharedCanvas) | Reusable creative-document and rendering components, including editing history, previews, and a growing native package. |
| [LVUI](https://github.com/iisacc-Justmoong/LVUI) | Declarative UI and native component work that separates visual behavior from platform-host services. |
| [iiMultimodalAgent](https://github.com/iisacc-Justmoong/iiMultimodalAgent) | C++23 agent orchestration, persistent sessions, permission-controlled tools, and opt-in local retrieval with source revisions. |

## Recent engineering work

- **Observable state across shared-library boundaries:** a common observation runtime keeps dependency collection consistent between an application and hosted model modules. [Design and contracts](https://github.com/iisacc-Justmoong/iiSDKCore/blob/master/docs/observable.md)
- **Storage continuity between applications:** Dreamscapes and Society share logical storage while preserving paths, identities, and existing files. Apple App Group behavior depends on the appropriate signing and entitlements. [Storage design](https://github.com/iisacc-Justmoong/Dreamscapes/blob/master/docs/SharedLogicalStorage.md)
- **Source-aware local retrieval:** revision tracking, replaceable embedding providers, and model-fingerprinted caches connect retrieval to agent workflows without treating citation formatting as proof of factual accuracy. [Retrieval design](https://github.com/iisacc-Justmoong/iiMultimodalAgent/blob/main/docs/Rag.md)

I am also developing native UI and canvas paths alongside existing Qt/QML applications. This is an ongoing migration, not a claim that every product or platform is already Qt-free.

## How I work

I define the intended behavior and architectural constraints, use AI coding tools to support implementation, and review the resulting code and integration. I value clear ownership, reproducible failures, useful tests, and documentation that distinguishes implemented behavior from work still awaiting verification.

**Core tools:** C++23 · Qt / QML · CMake · Git  
**Product and web:** Figma · SvelteKit · React · TypeScript

[Website](https://iisacc.com/) · [LinkedIn](https://www.linkedin.com/in/muyeong-yun-6488b0286/)

<details>
<summary>GitHub activity</summary>

<br>

<img src="https://github-readme-streak-stats.herokuapp.com/?user=iisacc-Justmoong&theme=tokyonight&hide_border=true" height="170" alt="GitHub contribution streak" />

<img src="https://github-readme-activity-graph.vercel.app/graph?username=iisacc-Justmoong&theme=tokyo-night&hide_border=true" alt="GitHub contribution activity graph" />

</details>
