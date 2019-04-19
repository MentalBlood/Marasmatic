#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <locale.h>
#define INITIAL_SIZE 5
#define INCREASE_RATE 5
#define NUMBER_OF_WORDS_IN_ONE_ELEMENT 3

int get_word(FILE *file, char *word, int n, int len)
{
	int c; char *i = word; int reading = 0, j = 0;
	while (i - word < len && j != n)
	{
		while (1)
		{
			c = fgetc(file);
			if (c != ' ' && c != '\n')
			{
				reading = 1;
				*i = c;
				++i;
			}
			else if (reading) break;
			if (feof(file)) return 1;
		}
		++j; *i = ' '; i++;
	}
	*i = 0;
	return 0;
}

typedef struct Word
{
	char *word;
	int n;
	struct Word **next, *left, *right;
} Word;

int N = 0;
int LINKS = 0;

Word* put_word(char *word, Word **last, Word **root)
{
	int c; Word **w = root, **w1;
	while (*w)
	{
		c = strcmp(word, (*w)->word);
		if (c > 0)
			w = &(*w)->right;
		else
			if (c < 0)
				w = &(*w)->left;
		else
			break;
	}
	if (!*w)
	{
		N++;
		*w = malloc(sizeof(Word)); (*w)->right = NULL;
		(*w)->left = NULL;
		(*w)->n = 0;
		c = strlen(word) + 1;
		(*w)->word = malloc(sizeof(char) * c);
		strcpy((*w)->word, word);
		if (!last)
			return *w;
	}
	else
	{
		c = 1;
		for (w1 = (*last)->next; w1 < (*last)->next + (*last)->n; w1++)
			if (*w1 == *w)
				c = 0;
		if (!c)
			return *w;
	}
	if (!(*last)->n)
		(*last)->next = malloc(sizeof(Word*)*INITIAL_SIZE);
	else
		if (!(((*last)->n - INITIAL_SIZE) % INCREASE_RATE))
			(*last)->next = realloc((*last)->next, sizeof(Word*) * ((*last)->n + INCREASE_RATE));
	(*last)->next[(*last)->n] = *w;
	(*last)->n++;
	LINKS++;
	return *w;
}

int process_file(FILE *file, Word **root)
{
	printf("Processing file...\n");
	char word[120];
	Word *last;
	unsigned long int n = 1;
	get_word(file, word, 1, 3);
	last = put_word(word, 0, root);
	while (!get_word(file, word, n % 2 + 1, NUMBER_OF_WORDS_IN_ONE_ELEMENT))
	{
		last = put_word(word, &last, root);
		++n;
	}
	return n;
}

void print_all(Word *root)
{
	if (!root) return;
	print_all(root->left); puts(root->word); print_all(root->right);
}

int depth(Word *root, int n)
{
	if (!root) return n;
	int n1, n2;
	n1 = depth(root->left, n + 1); n2 = depth(root->right, n + 1);
	if (n1 > n2) return n + n1; else return n + n2;
}

Word* random_word(Word *root, int n)
{
	if (!root) return 0;
	if (!n) return root;
	if (rand() % 2)
	{
		Word *w = random_word(root->left, n - 1);
		if (!w)
			return random_word(root->right, n - 1);
		else
			return w;
	}
	else
	{
		Word *w = random_word(root->right, n - 1);
		if (!w)
			return random_word(root->left, n - 1);
		else
			return w;
	}
	return 0;
}

Word** print_random(Word **root, int n, char **s)
{
	if (!(*root)->n) return 0;
	if (!n) return root;
	Word **p;
	int i = rand() % (*root)->n;
	int j = i, k = 1;
	for (; (i != j) || k; i = (i + 1) % (*root)->n)
	{
		k = 0;
		p = print_random(&(*root)->next[i], n-1, s);
		if (p)
			if (*p)
			{
				if (!s[n])
					s[n] = malloc(sizeof(char) * (strlen((*root)->word) + 1));
				else
					s[n] = realloc(s[n], sizeof(char) * (strlen((*root)->word) + 1));
				strcpy(s[n], (*root)->word);
				return &(*root)->next[i];
			}
	}
	return 0;
}

int main(void)
{
	setlocale(LC_ALL,"");
	char file_name[100];
	printf("File name: ");
	scanf("%s", file_name);
	
	FILE *file = fopen(file_name, "rb");
	if (!file)
	{
		printf("no such file\n");
		return 1;
	}
	
	Word *tree = NULL, *t;
	int n = process_file(file, &tree);
	printf("%d of total %d words loaded, %d links\n", n - N, n, LINKS);
	
	int d = depth(tree, 0);
	printf("depth = %d\n", d);
	
	char **s, **i;
	
	srand(time(0));
	while (1)
	{
		printf("Number of words: ");
		scanf("%d", &n);
		
		s = calloc(sizeof(char*), n);
		while (1)
		{
			t = random_word(tree, 10);
			if (t) break;
		}
		s[n] = NULL;
		while (!s[n])
			print_random(&t, n, s);
		for (i = s+n-1; i > s; i--)
			printf("%s", *i);
		printf("\n");
	}
	
	return 0;
}
