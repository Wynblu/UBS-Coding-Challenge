all: stack shellcode

stack: stack.c
	gcc -g -no-pie -fno-stack-protector stack.c -o stack

shellcode: shellcode.c
	gcc -g -fno-stack-protector -z execstack shellcode.c -o shellcode

clean:
	rm -rf stack shellcode
