from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .functions import searchProject, paginateProjects

from django.contrib import messages

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.


def projects(request):
    projects, search_query = searchProject(request)

    custom_range, projects = paginateProjects(request, projects, 6)

    #project = Project.objects.get()
    #project = get_object_or_404(Project, id=request.user.id)

    image_url = project_image_url(request, projects)

    context = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)


def project_image_url(request, image_data):
    # This function generates a URL to serve the image
    # The URL should be pointing to a view that serves the image data

    return request.build_absolute_uri(f'/project_image/{request.user.id}/')


def serve_project_image(request, pk):
    project = get_object_or_404(Project, id=pk)
    image_data = project.featured_image
    if image_data:
        response = HttpResponse(image_data, content_type='image/jpeg')
        return response
    else:
        return HttpResponse(status=404)


def singleProject(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        messages.success(request, 'Review Added Successfully!')
        return redirect('single_project', pk=projectObj.id)
        #Update project vote count:


    context = {'project': projectObj, 'form': form}
    return render(request, 'projects/single-project.html', context)

@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newTags').replace(',', " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():

            file = request.FILES['featured_image']
            project_image = file.read()

            project = form.save(commit=False)
            project.featured_image = project_image
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newtags = request.POST.get('newTags').replace(',', " ").split()

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')

    context = {'form': form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    context = {'object': project}
    return render(request, 'delete_template.html', context)


