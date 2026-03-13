#include <stdio.h>
#include <stdlib.h>

typedef struct {
  char *data;
  unsigned int length;
  unsigned int capacity;
} SString;

void initSString(SString *s) {
  s->capacity = 4;
  s->length = 0;
  s->data = (char *)malloc(s->capacity * sizeof(char));
  if (s->data == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(1);
  }
}

void appendChar(SString *s, char c) {
  if (s->length == s->capacity) {
    s->capacity *= 2;
    char *new_data = (char *)realloc(s->data, s->capacity * sizeof(char));
    if (new_data == NULL) {
      fprintf(stderr, "Memory reallocation failed\n");
      exit(1);
    }
    s->data = new_data;
  }
  s->data[s->length] = c;
  s->length++;
}

void clearSString(SString *s) {
  s->length = 0;
}

void printSString(SString *s) {
  for (unsigned int i = 0; i < s->length; i++) {
    putchar(s->data[i]);
  }
  putchar('\n');
}

void displaySString(SString *s) {
  printf("String: \"");
  for (unsigned int i = 0; i < s->length; i++) {
    putchar(s->data[i]);
  }
  printf("\"\n");
  printf("Length: %u\n", s->length);
  printf("Capacity: %u\n", s->capacity);
}

SString* getTarget(char id, SString *a, SString *b, SString *c, SString *d) {
  if (id == 'a') return a;
  if (id == 'b') return b;
  if (id == 'c') return c;
  if (id == 'd') return d;
  return NULL;
}

void readInputToString(SString *s, int append) {
  if (!append) clearSString(s);
  
  int c = getchar();
  
  while (c != EOF && (c == ' ' || c == '\n' || c == '\t' || c == '\r')) {
    c = getchar();
  }

  if (c == '"') {
    while ((c = getchar()) != EOF && c != '"') {
      appendChar(s, (char)c);
    }
  } else if (c != EOF) {
    while (c != EOF && c != ' ' && c != '\n' && c != '\t' && c != '\r') {
      appendChar(s, (char)c);
      c = getchar();
    }
  }
}

int main() {
  SString a, b, c, d;
  initSString(&a);
  initSString(&b);
  initSString(&c);
  initSString(&d);

  char cmd;
  while (scanf(" %c", &cmd) == 1) {
    if (cmd == 'q') break;

    if (cmd == 'r' || cmd == 'a' || cmd == 'p' || cmd == 'd') {
      char t_id;
      scanf(" %c", &t_id);
      SString *target = getTarget(t_id, &a, &b, &c, &d);

      if (cmd == 'r') {
        readInputToString(target, 0);
      } else if (cmd == 'a') {
        readInputToString(target, 1);
      } else if (cmd == 'p') {
        printSString(target);
      } else if (cmd == 'd') {
        displaySString(target);
      }
    } else if (cmd == 'c') {
      char t1_id, t2_id, t3_id;
      scanf(" %c %c %c", &t1_id, &t2_id, &t3_id);
      SString *t1 = getTarget(t1_id, &a, &b, &c, &d);
      SString *t2 = getTarget(t2_id, &a, &b, &c, &d);
      SString *t3 = getTarget(t3_id, &a, &b, &c, &d);

      clearSString(t1);
      for (unsigned int i = 0; i < t2->length; i++) {
        appendChar(t1, t2->data[i]);
      }
      for (unsigned int i = 0; i < t3->length; i++) {
        appendChar(t1, t3->data[i]);
      }
    }
  }

  free(a.data);
  free(b.data);
  free(c.data);
  free(d.data);
  
  return 0;
}