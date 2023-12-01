

for file in $(find ./notebooks/optimization/eco_pants_examples -type f -name '*.ipynb')
do
  echo $file
  nbconvert_file=$(echo $file | sed 's/.ipynb/.nbconvert.ipynb/')
  jupyter nbconvert --to notebook --allow-errors --execute $file
  mv -f $nbconvert_file $file
done
