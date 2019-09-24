# Warmup - Pwn - 29 solves

## Reversing

File PE khá đơn giản, tại hàm main sẽ gọi tới 1 hàm func, sau đó sẽ đọc input vào biến Buffer bằng hàm ReadFile.

```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char Buffer; // [esp+0h] [ebp-44h]

  j_init();
  j_printf(aWelcomeBanner, Buffer);
  j_func();
  j_printf(aDidYouMakeSome, Buffer);
  ReadFile(hStdin, &Buffer, 0x60u, 0, 0);
  return 0;
}
```

Bên trong hàm func thực hiện đọc input từ người dùng, sau đó in ra input đã nhập:

```
  v0 = GetProcessHeap();
  hHeap = (char)v0;
  lpBuffer = HeapAlloc(v0, 8u, 0x150u);
  j_printf(&v6, hHeap);
  ReadFile(hStdin, lpBuffer, 0x150u, 0, 0);
  j_printf(lpBuffer, v3);
  j_printf(&unk_463018, v4);
  return 0;
```

## Bugs

Ở đây, có 2 bug khá rõ ràng:

Một là bug formatstring bên trong hàm func:

```
  ReadFile(hStdin, lpBuffer, 0x150u, 0, 0);
  j_printf(lpBuffer, v3);
```

Bug còn lại là buffer overflow bên trong hàm main. Sau khi gọi hàm func, chương trình sử dụng ReadFile để đọc tối đa 0x150 ký tự vào biến Buffer (chứa tối đa 0x44 ký tự)(thông tin hàm ReadFile có thể xem tại [đây](https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-readfile)):

```
  char Buffer; // [esp+0h] [ebp-44h]
  ...
  ReadFile(hStdin, &Buffer, 0x60u, 0, 0);
```

## Exploitation

Chương trình cung cấp sẵn một hàm có nhiệm vụ đọc flag nằm ở offset 0x406c80 (hoặc có thể sử dụng lệnh jump tới hàm này ở offset 0x4023bf)

Chương trình sử dụng stack canary để bảo vệ stack overflow, tuy nhiên có thể sử dụng formatstring để leak giá trị canary. Đồng thời leak địa chỉ hàm main để tính địa chỉ của hàm catFlag






