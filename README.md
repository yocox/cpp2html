### cpp2html - A C++ high-lighter to html ###

Input C++ source file, output highlight html.

### Usage ###

For example, you have a `test.cc` with content

    #include <iostream>
    
    int main()
    {
        // comment
        std::cout << "Hello world!" << std::endl;
        std::cout << 3.14 << std::endl;
    }

type in command line:

    cpp2html.py test.cc
  
you get a html `test.cc.html` looks like 

![highlighted](https://raw.github.com/yocox/cpp2html/master/images/cpp2html.png)

### id-aware coloring ###

You can see the color of `std` is different to `cout` and `endl`. It is not because the highlighter can detect namespace. It is because the highlighter hash eash id into a color. So, same id will has the same color. It is really useless, just make the code much more difficult to read, and, there is no option to turn this feature off.
