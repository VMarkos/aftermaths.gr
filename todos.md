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
- [ ] Fix landing page `index.rst` to show the latest 'Aftermaths' post.
- [ ] Create, optionally, a "Latest" category where the five last posts are displayed.
- [ ] Fix innternal links which appear to point to the wrong files. Maybe:
    - Loop through all files and links per file.
    - For each link to an `.rst` file, search for it in the current structure and substitute its absolute path.

## Notes

1. All unaddressed issues have to be examined on a post-by-post basis.
