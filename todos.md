## Fixes

- [x] Youtube embeddings do not work
    - [ ] This might be a localhost issue.
- [ ] Quotations appear like double paragraphs (?) using some sort of <p> tag.
- [x] Greek double quote should be apostrophe / keraia.
- [x] Images inside articles, e.g., "Does it Have a Global Maximum?" do not render - the alt text is shown.
- [x] The "aligned" environment is not rendered, resulting into monstrously long equations.
    - [ ] It remains to verify all posts have been updated accordingly.
- [x] There is a "Misplaced &" error, maybe due to colouring (?), e.g., in "Reductio ad Absurdum #not".
- [ ] Inline or display math in lists sometimes appear as plain text, e.g., in "The second order equation".
- [x] No favicon shows.
- [x] Table captions appear erroneously as figcaptions, e.g., in "The Collatz Conjecture (1)"
- [x] Python code blocks are not styled, e.g., in "The Collatz Conjecture (2)".
- [x] Some central pictures do not show, e.g., in "The Most Beutiful Derivative?".
- [ ] Various math rendering issues in "The Most Beautiful Derivative?".
- [x] Fix `wp-block-syntax-highlighter-code` blocks appearing all over the place, e.g., in tikz posts.
- [x] Check why side toc does not render the same in all pages, maybe needs make clean first.
- [x] Polish site index structure.
- [x] Fix broken yt links.
- [x] Fix landing page `index.rst` to show the latest 'Aftermaths' post.
- [x] Create, optionally, a "Latest" category where the five last posts are displayed.
- [x] In "recently", exclude any drafts.
- [x] Fix internal links which appear to point to the wrong files. Maybe:
    - Loop through all files and links per file.
    - For each link to an `.rst` file, search for it in the current structure and substitute its absolute path.
- [x] LaTeX formatting in Tikz posts.
- [x] Navigation links.
- [x] Translate 'On this page' to Greek.
- [x] Create contact page.
    - [x] Fix css for contact page by ammending the custom CSS file accordingly.
- [x] Fix the global link for tests pointing to the actual tests page.
- [x] Fix the global link for teaching materials
- [x] Locate and handle hardcoded `afteramths.gr` and `aftermathsgr.wordpress.com` references.
- [x] Fig `tag` and `category` links.
- [x] There are some wp-related code blocks in tikz posts.
    - [ ] Maybe fixed? I could not grep those.
- [x] Shorten EPAL C TOC tree.
- [x] Fix images that are not found, e.g., `.png?w=\d{3}`
- [x] Check why `/panellinies` is not found as a document.
- [x] Fix the following (missing).
- [x] Fix broken youtube links (2 arguments instead of 1, e.g., remove spacing)
- [ ] `contents.rst` should be updated with just one new line of the most recent post; no duplicates


## Notes

1. All unaddressed issues have to be examined on a post-by-post basis.
