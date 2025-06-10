# usb gadget module configuration for [zero-hid](https://github.com/thewh1teagle/zero-hid)

To be able to use `zero-hid` package
it's necessary to change some configuration on the kernel.

### Install / remove the module
clone the repo if you haven't yet
```bash
cd ~ && (sudo rm -rf zero-hid >/dev/null 2>&1 || true) && git clone -b main https://github.com/cgu-tech/zero-hid.git
```

Execute `installer`
```bash
cd zero-hid/usb_gadget && sudo ./installer
```
