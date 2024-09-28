void vuln() {
  char small_buffer[96];
  read(0, small_buffer, 96);
  int (*ret)() = (int (*)())small_buffer;
  ret();
}

int main(int argc, char **argv, char **envp) {
  vuln();
  puts("Bye!");
}
