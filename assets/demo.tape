# vhs assets/demo.tape  ->  assets/demo.gif
Output assets/demo.gif

Set Shell "bash"
Set FontSize 17
Set Width 1100
Set Height 400
Set Theme "Catppuccin Mocha"
Set Padding 24
Set TypingSpeed 35ms

Hide
Type "export PATH=$PWD/.venv/bin:$PATH; rm -rf out; clear"
Enter
Show

Type "pdftool merge sample_files/page_a.pdf sample_files/page_b.pdf -o out/merged.pdf"
Sleep 400ms
Enter
Sleep 1.2s

Type "pdftool split sample_files/multi.pdf --ranges 1-2,3- -o out/split/"
Sleep 400ms
Enter
Sleep 1.2s

Type "pdftool watermark sample_files/multi.pdf --text CONFIDENTIAL -o out/draft.pdf"
Sleep 400ms
Enter
Sleep 1.2s

Type "pdftool fill sample_files/intake_form.pdf --data sample_files/sample_data.csv -o out/filled/"
Sleep 400ms
Enter
Sleep 2.5s
