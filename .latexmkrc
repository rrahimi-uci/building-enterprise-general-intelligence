$pdf_mode = 5;
$xelatex = 'xelatex -interaction=nonstopmode -halt-on-error -file-line-error %O %S';
$out_dir = 'latex/build';
$makeindex = 'makeindex -q -s latex/bookindex.ist -o %D %S';
