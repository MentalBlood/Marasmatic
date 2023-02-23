#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <locale.h>
#include <stdbool.h>

#define INITIAL_SIZE 5
#define INCREASE_RATE 5



bool get_word(FILE *file, char *word, size_t n, size_t len) {

	size_t c;
	size_t reading = 0;
	size_t j = 0;
	char *i = word;

	while (i - word < len && j != n) {
		while (1) {

			c = fgetc(file);

			if (c != ' ' && c != '\n') {
				reading = 1;
				*i = c;
				++i;
			} else if (reading)
				break;

			if (feof(file))
				return false;

		}
		j++;
		*i = ' ';
		i++;
	}
	*i = 0;

	return true;

}

typedef struct Word {
	char *word;
	int n;
	struct Word **next, *left, *right;
} Word;

Word* put_word(char *word, Word **last, Word **root) {

	int c;
	Word **w1;
	Word **w = root;

	while (*w) {
		c = strcmp(word, (*w)->word);
		if (c > 0)
			w = &(*w)->right;
		else if (c < 0)
			w = &(*w)->left;
		else
			break;
	}

	if (!*w) {

		*w = malloc(sizeof(Word));
		(*w)->right = NULL;
		(*w)->left = NULL;
		(*w)->n = 0;

		c = strlen(word) + 1;
		(*w)->word = malloc(sizeof(char) * c);
		strcpy((*w)->word, word);
		if (!last)
			return *w;

	} else {
		c = 1;
		for (w1 = (*last)->next; w1 < (*last)->next + (*last)->n; w1++)
			if (*w1 == *w)
				c = 0;
		if (!c)
			return *w;
	}

	if (!(*last)->n)
		(*last)->next = malloc(sizeof(Word*)*INITIAL_SIZE);
	else if (!(((*last)->n - INITIAL_SIZE) % INCREASE_RATE))
		(*last)->next = realloc((*last)->next, sizeof(Word*) * ((*last)->n + INCREASE_RATE));

	(*last)->next[(*last)->n] = *w;
	(*last)->n++;

	return *w;

}

Word* process_file(FILE *file, size_t word_size) {

	Word** root = (Word**)malloc(sizeof(Word*) * 1);
	*root = NULL;

	char* word = (char*)malloc(sizeof(char) * 64 * word_size);
	Word* last = NULL;
	size_t n = 0;

	while (get_word(file, word, n % 2 + 1, word_size))
	{
		last = put_word(word, last ? &last : NULL, root);
		n++;
	}

	free(word);

	return *root;

}


Word* random_word(Word *root, size_t n) {

	if (!root)
		return NULL;

	if (!n)
		return root;

	size_t r = rand() % 2;
	Word *w = random_word(r ? root->left : root->right, n - 1);
	if (w)
		return w;
	else
		return random_word(!r ? root->left : root->right, n - 1);

	return NULL;

}

Word** print_random(Word **root, size_t n) {

	if (!(*root)->n)
		return NULL;

	if (!n)
		return root;

	size_t i = rand() % (*root)->n;
	while (1) {

		if (print_random(&(*root)->next[i], n-1)) {
			printf("%s", (*root)->word);
			return &(*root)->next[i];
		}

		i = (i + 1) % (*root)->n;

	}

	return NULL;

}

int main(const size_t argc, const char** argv) {

	size_t texts;
	if (argc < 5) {
		printf("no number of texts provided, exiting\n");
		return 1;
	} else {
		sscanf(argv[4], "%zu", &texts);
	}

	size_t print;
	if (argc < 4) {
		printf("no number of words to print provided, exiting\n");
		return 1;
	} else {
		sscanf(argv[3], "%zu", &print);
	}

	size_t size;
	if (argc < 3) {
		printf("no size of 'word' (in real words), exiting\n");
		return 1;
	} else {
		sscanf(argv[2], "%zu", &size);
	}

	char* path;
	if (argc < 2) {
		printf("no file path provided, exiting\n");
		return 1;
	} else {
		path = (char*)malloc(sizeof(char) * (strlen(argv[1]) + 1));
		strcpy(path, argv[1]);
	}

	setlocale(LC_ALL, "");
	FILE *file = fopen(path, "rb");
	if (!file) {
		printf("no such file, exiting\n");
		return 2;
	}

	Word *root = process_file(file, size);
	Word *random;
	srand(time(0));
	for (; texts; texts--) {

		do {
			random = random_word(root, 10);
		} while (!random);

		print_random(&random, print);

		putc('\n', stdout);
		putc('\n', stdout);

	}

	return 0;

}
