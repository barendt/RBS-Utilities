#include "Python.h"

static PyObject *
overlap_count(PyObject *self, PyObject *args) {
  int i = 0;
  int j = 0;
  int k = 0;
  int count = 0;
  int needle_length;
  const char* haystack;
  const char* needle;

  if (!PyArg_ParseTuple(args, "ss", &haystack, &needle)) {
    return NULL;
  }

  needle_length = strlen(needle);

  while (haystack[i+needle_length-1] != EOF) {
    j = i;
    for (k=0; k<needle_length; k++) {
      if (haystack[j] != needle[k]) {
        break;
      }
      if (k == needle_length) {
        count++;
      }
      j++;
    }
    i++;
  }
}
