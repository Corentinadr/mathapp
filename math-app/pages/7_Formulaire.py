import streamlit as st

from ui.config import configurer_page

configurer_page("Formulaire")

st.title("Formulaire")
st.caption("Résultats et formules à connaître par cœur.")

tab_der, tab_prim, tab_lim, tab_dl, tab_trigo = st.tabs(
    ["Dérivées", "Primitives", "Limites", "Développements limités", "Trigonométrie"]
)

# ---------------------------------------------------------------------------
with tab_der:
    st.subheader("Dérivées usuelles")
    st.markdown(
        r"""
| $f(x)$ | $f'(x)$ | Domaine |
|---|---|---|
| $x^n$ (n ∈ ℝ) | $n\, x^{n-1}$ | ℝ ou ℝ\* selon $n$ |
| $\sqrt{x}$ | $\dfrac{1}{2\sqrt{x}}$ | $x > 0$ |
| $\dfrac{1}{x}$ | $-\dfrac{1}{x^2}$ | $x \neq 0$ |
| $e^x$ | $e^x$ | ℝ |
| $a^x$ | $a^x \ln a$ | ℝ |
| $\ln x$ | $\dfrac{1}{x}$ | $x > 0$ |
| $\log_a x$ | $\dfrac{1}{x \ln a}$ | $x > 0$ |
| $\sin x$ | $\cos x$ | ℝ |
| $\cos x$ | $-\sin x$ | ℝ |
| $\tan x$ | $1 + \tan^2 x = \dfrac{1}{\cos^2 x}$ | $x \neq \tfrac{\pi}{2} + k\pi$ |
| $\arcsin x$ | $\dfrac{1}{\sqrt{1-x^2}}$ | $|x| < 1$ |
| $\arccos x$ | $-\dfrac{1}{\sqrt{1-x^2}}$ | $|x| < 1$ |
| $\arctan x$ | $\dfrac{1}{1+x^2}$ | ℝ |
| $\sinh x$ | $\cosh x$ | ℝ |
| $\cosh x$ | $\sinh x$ | ℝ |
"""
    )

    st.subheader("Règles de dérivation")
    st.markdown(
        r"""
- **Somme** : $(u + v)' = u' + v'$
- **Produit** : $(u \cdot v)' = u'v + u v'$
- **Quotient** : $\left(\dfrac{u}{v}\right)' = \dfrac{u'v - u v'}{v^2}$
- **Composition (chaîne)** : $(f \circ g)'(x) = g'(x) \cdot f'\bigl(g(x)\bigr)$
- **Réciproque** : $(f^{-1})'(y) = \dfrac{1}{f'\bigl(f^{-1}(y)\bigr)}$
"""
    )

# ---------------------------------------------------------------------------
with tab_prim:
    st.subheader("Primitives usuelles")
    st.info("On note $F(x) + C$ la primitive générale ; on omet le $+C$ dans le tableau.")
    st.markdown(
        r"""
| $f(x)$ | $F(x)$ | Conditions |
|---|---|---|
| $x^n$ ($n \neq -1$) | $\dfrac{x^{n+1}}{n+1}$ | — |
| $\dfrac{1}{x}$ | $\ln \lvert x \rvert$ | $x \neq 0$ |
| $e^{ax}$ | $\dfrac{1}{a} e^{ax}$ | $a \neq 0$ |
| $\sin(ax)$ | $-\dfrac{1}{a}\cos(ax)$ | $a \neq 0$ |
| $\cos(ax)$ | $\dfrac{1}{a}\sin(ax)$ | $a \neq 0$ |
| $\tan x$ | $-\ln \lvert \cos x \rvert$ | — |
| $\dfrac{1}{\cos^2 x}$ | $\tan x$ | — |
| $\dfrac{1}{1+x^2}$ | $\arctan x$ | — |
| $\dfrac{1}{\sqrt{1-x^2}}$ | $\arcsin x$ | $|x| < 1$ |
| $\dfrac{1}{x^2 - a^2}$ | $\dfrac{1}{2a}\ln\left\lvert\dfrac{x-a}{x+a}\right\rvert$ | $a \neq 0$ |
| $\dfrac{u'(x)}{u(x)}$ | $\ln \lvert u(x) \rvert$ | $u \neq 0$ |
| $u'(x)\, u(x)^n$ ($n \neq -1$) | $\dfrac{u(x)^{n+1}}{n+1}$ | — |
| $u'(x)\, e^{u(x)}$ | $e^{u(x)}$ | — |
"""
    )

    st.subheader("Techniques d'intégration")
    st.markdown(
        r"""
- **Intégration par parties** : $\displaystyle \int u'\, v\, dx = uv - \int u\, v'\, dx$
- **Changement de variable** : si $u = \varphi(x)$, $\displaystyle \int f(\varphi(x))\, \varphi'(x)\, dx = \int f(u)\, du$
- **Décomposition en éléments simples** pour les fractions rationnelles.
"""
    )

# ---------------------------------------------------------------------------
with tab_lim:
    st.subheader("Limites usuelles en 0")
    st.markdown(
        r"""
| Expression | Limite en 0 |
|---|---|
| $\dfrac{\sin x}{x}$ | $1$ |
| $\dfrac{1 - \cos x}{x^2}$ | $\dfrac{1}{2}$ |
| $\dfrac{\tan x}{x}$ | $1$ |
| $\dfrac{e^x - 1}{x}$ | $1$ |
| $\dfrac{\ln(1+x)}{x}$ | $1$ |
| $\dfrac{(1+x)^\alpha - 1}{x}$ | $\alpha$ |
| $\dfrac{\arctan x}{x}$ | $1$ |
| $\dfrac{\arcsin x}{x}$ | $1$ |
"""
    )

    st.subheader("Croissances comparées en +∞")
    st.markdown(
        r"""
Pour tout $\alpha > 0$ et $\beta > 0$ :

- $\dfrac{\ln^\beta x}{x^\alpha} \xrightarrow[x \to +\infty]{} 0$   *(logarithme battu par puissance)*
- $\dfrac{x^\alpha}{e^{\beta x}} \xrightarrow[x \to +\infty]{} 0$   *(puissance battue par exponentielle)*
- $x^\alpha \ln^\beta x \xrightarrow[x \to 0^+]{} 0$
"""
    )

    st.subheader("Limites remarquables")
    st.markdown(
        r"""
- $\displaystyle\lim_{x \to +\infty} \left(1 + \dfrac{1}{x}\right)^x = e$
- $\displaystyle\lim_{x \to 0} \left(1 + x\right)^{1/x} = e$
- **Formes indéterminées** : $\dfrac{0}{0}$, $\dfrac{\infty}{\infty}$, $0 \times \infty$, $\infty - \infty$, $0^0$, $\infty^0$, $1^\infty$
"""
    )

# ---------------------------------------------------------------------------
with tab_dl:
    st.subheader("Formule de Taylor-Young")
    st.latex(
        r"f(x) = \sum_{k=0}^{n} \dfrac{f^{(k)}(a)}{k!} (x-a)^k + o\bigl((x-a)^n\bigr)"
    )
    st.caption("En 0, on parle de développement limité (DL) ; c'est le cas Maclaurin.")

    st.subheader("DL usuels en 0")
    st.markdown(
        r"""
| $f(x)$ | Développement limité en 0 |
|---|---|
| $e^x$ | $1 + x + \dfrac{x^2}{2!} + \dfrac{x^3}{3!} + \dots + \dfrac{x^n}{n!} + o(x^n)$ |
| $\sin x$ | $x - \dfrac{x^3}{3!} + \dfrac{x^5}{5!} - \dots + (-1)^n \dfrac{x^{2n+1}}{(2n+1)!} + o(x^{2n+1})$ |
| $\cos x$ | $1 - \dfrac{x^2}{2!} + \dfrac{x^4}{4!} - \dots + (-1)^n \dfrac{x^{2n}}{(2n)!} + o(x^{2n})$ |
| $\tan x$ | $x + \dfrac{x^3}{3} + \dfrac{2 x^5}{15} + o(x^5)$ |
| $\sinh x$ | $x + \dfrac{x^3}{3!} + \dfrac{x^5}{5!} + \dots + o(x^{2n+1})$ |
| $\cosh x$ | $1 + \dfrac{x^2}{2!} + \dfrac{x^4}{4!} + \dots + o(x^{2n})$ |
| $\ln(1+x)$ | $x - \dfrac{x^2}{2} + \dfrac{x^3}{3} - \dots + (-1)^{n+1}\dfrac{x^n}{n} + o(x^n)$ |
| $\dfrac{1}{1-x}$ | $1 + x + x^2 + \dots + x^n + o(x^n)$ |
| $\dfrac{1}{1+x}$ | $1 - x + x^2 - \dots + (-1)^n x^n + o(x^n)$ |
| $(1+x)^\alpha$ | $1 + \alpha x + \dfrac{\alpha(\alpha-1)}{2!} x^2 + \dots + \dbinom{\alpha}{n} x^n + o(x^n)$ |
| $\sqrt{1+x}$ | $1 + \dfrac{x}{2} - \dfrac{x^2}{8} + \dfrac{x^3}{16} + o(x^3)$ |
| $\dfrac{1}{\sqrt{1+x}}$ | $1 - \dfrac{x}{2} + \dfrac{3 x^2}{8} - \dfrac{5 x^3}{16} + o(x^3)$ |
| $\arctan x$ | $x - \dfrac{x^3}{3} + \dfrac{x^5}{5} - \dots + (-1)^n \dfrac{x^{2n+1}}{2n+1} + o(x^{2n+1})$ |
| $\arcsin x$ | $x + \dfrac{x^3}{6} + \dfrac{3 x^5}{40} + o(x^5)$ |
"""
    )

# ---------------------------------------------------------------------------
with tab_trigo:
    st.subheader("Identités fondamentales")
    st.markdown(
        r"""
- $\cos^2 x + \sin^2 x = 1$
- $1 + \tan^2 x = \dfrac{1}{\cos^2 x}$
- $\cos(-x) = \cos x$, $\sin(-x) = -\sin x$, $\tan(-x) = -\tan x$
"""
    )

    st.subheader("Formules d'addition")
    st.markdown(
        r"""
- $\cos(a + b) = \cos a \cos b - \sin a \sin b$
- $\cos(a - b) = \cos a \cos b + \sin a \sin b$
- $\sin(a + b) = \sin a \cos b + \cos a \sin b$
- $\sin(a - b) = \sin a \cos b - \cos a \sin b$
- $\tan(a + b) = \dfrac{\tan a + \tan b}{1 - \tan a \tan b}$
"""
    )

    st.subheader("Duplication")
    st.markdown(
        r"""
- $\cos(2x) = \cos^2 x - \sin^2 x = 2\cos^2 x - 1 = 1 - 2\sin^2 x$
- $\sin(2x) = 2 \sin x \cos x$
- $\tan(2x) = \dfrac{2 \tan x}{1 - \tan^2 x}$
"""
    )

    st.subheader("Linéarisation (à partir de la duplication)")
    st.markdown(
        r"""
- $\cos^2 x = \dfrac{1 + \cos(2x)}{2}$
- $\sin^2 x = \dfrac{1 - \cos(2x)}{2}$
"""
    )

    st.subheader("Passage par la tangente de l'arc moitié")
    st.markdown(
        r"""
Avec $t = \tan\dfrac{x}{2}$ :

- $\sin x = \dfrac{2t}{1+t^2}$
- $\cos x = \dfrac{1 - t^2}{1 + t^2}$
- $\tan x = \dfrac{2t}{1 - t^2}$
"""
    )
