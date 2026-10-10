class Cell {
    /*
        Simple class describing a cell in a magic square:
            * `#row` is the row of the cell, starting from top = 0;
            * `#col` is the column of the cell, starting from left = 0;
            * `#value` is the value of the cell, with empty = 0.
    */

    #row;
    #col;
    #value;
    
    constructor(row, col) {
        this.#row = row;
        this.#col = col;
        this.#value = 0;
    }

    // Getters
    get row() {
        return this.#row;
    }

    get col() {
        return this.#col;
    }

    get value() {
        return this.#value;
    }

    // Setters
    set value(x) {
        this.#value = x;
    }
}

class MagicSquare {
    /*
        Implementation of a magic square board:
            * `#n` corresponds to the size of the problem, i.e., the side of the square;
            * `#magicNumber` corresponds to the sum each row, column and diagonal should add up to;
            * `#cells` is an NxN 1-D array containing all cells of the board.
    */

    #n;
    #magicNumber;
    #cells;
    
    constructor(n, magicNumber) {
        this.#n = n;
        this.#magicNumber = magicNumber;
        this.#cells = [];
        for (let i = 0; i < this.#n * this.#n; i++) {
            this.#cells.push(new Cell(Math.floor(i / this.#n), i % this.#n));
        }
    }

    set magicNumber(x) {
        this.#magicNumber = x;
    }

    get magicNumber() {
        return this.#magicNumber;
    }

    setValue(row, col, val) {
        this.#cells[row * this.#n + col].value = val;
    }

    sumOfRow(row) {
        if (row < 0 || row >= this.#n) {
            return -1;
        }
        let sum = 0;
        for (let i = row * this.#n; i < row * this.#n + this.#n; i++) {
            sum += this.#cells[i].value;
        }
        return sum;
    }

    sumOfCol(col) {
        if (col < 0 || col >= this.#n) {
            return -1;
        }
        let sum = 0;
        for (let i = 0; i < this.#n; i++) {
            sum += this.#cells[this.#n * i + col].value;
        }
        return sum;
    }

    sumOfDiag(diag) { // diag = 1 | -1 (1 = main, -1 = sec)
        if (diag !== 1 && diag !== -1) {
            return -1;
        }
        let sum = 0;
        if (diag === 1) {
            for (let i = 0; i < this.#n; i++) {
                sum += this.#cells[this.#n * i + i].value;
            }
            return sum;
        }
        for (let i = 0; i < this.#n; i++) {
            sum += this.#cells[this.#n * i + this.#n - i - 1].value;
        }
        return sum;
    }

    isSolved() {
        for (let i = 0; i < this.#n; i++) {
            if (this.sumOfCol(i) !== this.#magicNumber) {
                return false;
            }
            if (this.sumOfRow(i) !== this.#magicNumber) {
                return false;
            }
        }
        if (this.sumOfDiag(1) !== this.#magicNumber) {
            return false;
        }
        if (this.sumOfDiag(-1) !== this.#magicNumber) {
            return false;
        }
        return true;
    }
}