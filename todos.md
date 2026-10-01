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
- [ ] LaTeX formatting in Tikz posts.
- [x] Navigation links.
- [ ] Translate 'On this page' to Greek.
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
- [ ] Fix the following:

```
    /home/bill/Documents/Projects/aftermaths/sphinx/docs/Διδακτικό-Υλικό/Α-Λυκείου/Άλγεβρα/index.rst:24: WARNING: unknown document: 'Εξισώσεις-και-ανισώσεις-Α-Βαθμού/index' [ref.doc]
/home/bill/Documents/Projects/aftermaths/sphinx/docs/Διδακτικό-Υλικό/Α-Λυκείου/Άλγεβρα/Σημειώσεις/ένα-μικρό-quiz-στην-άλγεβρα.rst:22: WARNING: unknown document: 'https://docs.google.com/forms/d/e/1FAIpQLSeRDBIyjWoyM_LAdqUftZ3c-wCwBxhGqGG37UvQlf4PfUlnIA/viewform?usp=sf_link' [ref.doc]
/home/bill/Documents/Projects/aftermaths/sphinx/docs/Διδακτικό-Υλικό/Α-Λυκείου/Άλγεβρα/Συναρτήσεις/φύλλο-εργασίας-εισαγωγή-στις-συναρτή.rst:24: WARNING: unknown document: 'https://www.slideshare.net/ssuserbf550d' [ref.doc]
/home/bill/Documents/Projects/aftermaths/sphinx/docs/Διδακτικό-Υλικό/Α-Λυκείου/Γεωμετρία/κατασκευές-με-κανόνα-και-διαβήτη.rst:24: WARNING: unknown document: '/docs/Διδακτικό-Υλικό/Α-Λυκείου/Γεωμετρία' [ref.doc]
/home/bill/Documents/Projects/aftermaths/sphinx/docs/Διδακτικό-Υλικό/Β-Λυκείου/Άλγεβρα/Σημειώσεις/άλγεβρα-β-λυκείου-μάθημα-24ο.rst:24: WARNING: unknown document: '/άλγεβρα-α-λυκείου-μάθημα-24ο' [ref.doc]
/home/bill/Documents/Projects/aftermaths/sphinx/docs/Διδακτικό-Υλικό/Γ-ΓΕΛ/Μαθηματικά/Σημειώσεις/σημειώσεις-μαθηματικών-κεφάλαιο-πρώ.rst:32: WARNING: unknown document: 'contact' [ref.doc]
/home/bill/Documents/Projects/aftermaths/sphinx/docs/Διδακτικό-Υλικό/Γ-ΓΕΛ/Μαθηματικά/Συναρτήσεις/τα-λυμένα-θέμα3.rst:22: WARNING: unknown document: '/docs/Διδακτικό-Υλικό/Γ-ΓΕΛ/Μαθηματικά/Συναρτήσεις ' [ref.doc]
/home/bill/Documents/Projects/aftermaths/sphinx/docs/Τεστάκι-της-ημέρας/Α-Λυκείου/Απόλυτες-Τιμές/τεστάκι8-κι-άλλες-απόλυτες-τιμές.rst:24: WARNING: unknown document: '/home/bill/Documents/Projects/aftermaths/sphinx/docs/Τεστάκι-της-ημέρας/Α-Λυκείου/Απόλυτες-Τιμές/τεστάκι7-απόλυτες-τιμές' [ref.doc]
/home/bill/Documents/Projects/aftermaths/sphinx/docs/Τεστάκι-της-ημέρας/Α-Λυκείου/Εισαγωγή/τεστάκι4-παραστάσεις-και-λίγες-πράξε.rst:24: WARNING: unknown document: '/docs/Τεστάκι-της-ημέρας/Α-Λυκείου/Εισαγωγή/τεστάκι3-κι-άλλα-σύνολα ' [ref.doc]
```

## Notes

1. All unaddressed issues have to be examined on a post-by-post basis.
