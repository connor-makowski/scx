

for file in ./notebooks/*/*.ipynb
do
  echo $file
  nbconvert_file=$(echo $file | sed 's/.ipynb/.nbconvert.ipynb/')
  jupyter nbconvert --to notebook --allow-errors --execute $file
  mv -f $nbconvert_file $file
done
